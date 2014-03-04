# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implements a message controller that understands Marconi messages."""

from marconiclient.queues.v1 import core


# NOTE(flaper87): Consider moving the
# iterator into a common package.
class _MessageIterator(object):
    """Message iterator

    This iterator is not meant to be used outside
    the scope of this package. The iterator gets
    a dictionary as returned by the message listing
    endpoint and iterates over the messages in the
    `messages` key.

    If there are no messages left to return, the iterator
    will try to load more by following the `next` rel link
    type.

    The iterator raises a StopIteration exception if the server
    doesn't return more messages after a `next-page` call.

    :param client: The client instance used by the queue
    :type client: `v1.Client`
    :param messages: Response returned by the messages listing call
    :type messages: Dict
    """

    def __init__(self, queue, messages):
        self._queue = queue

        # NOTE(flaper87): Simple hack to
        # re-use the iterator for get_many_messages
        # and message listing.
        self._links = []
        self._messages = messages

        if isinstance(messages, dict):
            self._links = messages['links']
            self._messages = messages['messages']

    def __iter__(self):
        return self

    def _next_page(self):
        for link in self._links:
            if link['rel'] == 'next':
                # NOTE(flaper87): We already have the
                # ref for the next set of messages, lets
                # just follow it.
                messages = self._queue.client.follow(link['href'])

                # NOTE(flaper87): Since we're using
                # `.follow`, the empty result will
                # be None. Consider making the API
                # return an empty dict for consistency.
                if messages:
                    self._links = messages['links']
                    self._messages = messages['messages']
                    return
        raise StopIteration

    def __next__(self):
        try:
            msg = self._messages.pop(0)
        except IndexError:
            self._next_page()
            return self.next()
        return Message(self._queue, **msg)

    # NOTE(flaper87): Py2K support
    next = __next__


class Message(object):
    """A handler for Marconi server Message resources.
    Attributes are only downloaded once - at creation time.
    """
    def __init__(self, queue, href, ttl, age, body):
        self.queue = queue
        self.href = href
        self.ttl = ttl
        self.age = age
        self.body = body

        # NOTE(flaper87): Is this really
        # necessary? Should this be returned
        # by Marconi?
        # The url has two forms depending on if it has been claimed.
        # /v1/queues/worker-jobs/messages/5c6939a8?claim_id=63c9a592
        # or
        # /v1/queues/worker-jobs/messages/5c6939a8
        self._id = href.split('/')[-1]
        if '?' in self._id:
            self._id = self._id.split('?')[0]

    def __repr__(self):
        return '<Message id:{id} ttl:{ttl}>'.format(id=self._id,
                                                    ttl=self.ttl)

    @property
    def claim_id(self):
        if '=' in self.href:
            return self.href.split('=')[-1]

    def delete(self):
        req, trans = self.queue.client._request_and_transport()
        core.message_delete(trans, req, self.queue._name, self._id)
