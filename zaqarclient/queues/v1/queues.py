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

from zaqarclient.queues.v1 import claim as claim_api
from zaqarclient.queues.v1 import core
from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v1 import message


class Queue(object):

    def __init__(self, client, name, auto_create=True):
        self.client = client

        # NOTE(flaper87) Queue Info
        self._name = name
        self._metadata = None

        if auto_create:
            self.ensure_exists()

    def exists(self):
        """Checks if the queue exists."""
        req, trans = self.client._request_and_transport()
        return core.queue_exists(trans, req, self._name)

    def ensure_exists(self):
        """Ensures a queue exists

        This method is not race safe,
        the queue could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()
        core.queue_create(trans, req, self._name)

    def metadata(self, new_meta=None, force_reload=False):
        """Get metadata and return it

        :param new_meta: A dictionary containing
            an updated metadata object. If present
            the queue metadata will be updated in
            remote server.
        :type new_meta: `dict`
        :param force_reload: Whether to ignored the
            cached metadata and reload it from the
            server.
        :type force_reload: `bool`

        :returns: The queue metadata.
        """
        req, trans = self.client._request_and_transport()

        if new_meta:
            core.queue_set_metadata(trans, req, self._name, new_meta)
            self._metadata = new_meta

        # TODO(flaper87): Cache with timeout
        if self._metadata and not force_reload:
            return self._metadata

        self._metadata = core.queue_get_metadata(trans, req, self._name)
        return self._metadata

    @property
    def stats(self):
        req, trans = self.client._request_and_transport()
        return core.queue_get_stats(trans, req, self._name)

    def delete(self):
        req, trans = self.client._request_and_transport()
        core.queue_delete(trans, req, self._name)

    # Messages API

    def post(self, messages):
        """Posts one or more messages to this queue

        :param messages: One or more messages to post
        :type messages: `list` or `dict`

        :returns: A dict with the result of this operation.
        :rtype: `dict`
        """
        if not isinstance(messages, list):
            messages = [messages]

        req, trans = self.client._request_and_transport()

        # TODO(flaper87): Return a list of messages
        return core.message_post(trans, req,
                                 self._name, messages)

    def message(self, message_id):
        """Gets a message by id

        :param message_id: Message's reference
        :type message_id: `six.text_type`

        :returns: A message
        :rtype: `dict`
        """
        req, trans = self.client._request_and_transport()
        msg = core.message_get(trans, req, self._name,
                               message_id)
        return message.Message(self, **msg)

    def messages(self, *messages, **params):
        """Gets a list of messages from the server

        This method returns a list of messages, it can be
        used to retrieve a set of messages by id or to
        walk through the active messages by using the
        collection endpoint.

        The `messages` and `params` params are mutually exclusive
        and the former has the priority.

        :param messages: List of messages' ids to retrieve.
        :type messages: *args of `six.string_type`

        :param params: Filters to use for getting messages
        :type params: **kwargs dict.

        :returns: List of messages
        :rtype: `list`
        """
        req, trans = self.client._request_and_transport()

        # TODO(flaper87): Return a MessageIterator.
        # This iterator should handle limits, pagination
        # and messages deserialization.

        if messages:
            msgs = core.message_get_many(trans, req,
                                         self._name, messages)
        else:
            # NOTE(flaper87): It's safe to access messages
            # directly. If something wrong happens, the core
            # API will raise the right exceptions.
            msgs = core.message_list(trans, req,
                                     self._name,
                                     **params)

        return iterator._Iterator(self.client,
                                  msgs,
                                  'messages',
                                  message.create_object(self))

    def claim(self, id=None, ttl=None, grace=None,
              limit=None):
        return claim_api.Claim(self, id=id, ttl=ttl, grace=grace, limit=limit)


def create_object(parent):
    return lambda args: Queue(parent, args["name"], auto_create=False)
