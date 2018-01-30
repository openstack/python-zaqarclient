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
"""Implements a message controller that understands Zaqar messages."""

from zaqarclient.queues.v1 import core


class Message(object):
    """A handler for Zaqar server Message resources.

    Attributes are only downloaded once - at creation time.
    """
    def __init__(self, queue, ttl, age, body, href=None, id=None,
                 claim_id=None, claim_count=0, checksum=None):
        self.queue = queue
        self.href = href
        self.ttl = ttl
        self.age = age
        self.body = body
        self.claim_count = claim_count
        self.checksum = checksum

        # NOTE(flaper87): Is this really
        # necessary? Should this be returned
        # by Zaqar?
        # The url has two forms depending on if it has been claimed.
        # /v1/queues/worker-jobs/messages/5c6939a8?claim_id=63c9a592
        # or
        # /v1/queues/worker-jobs/messages/5c6939a8
        if id is None:
            self._id = href.split('/')[-1]
            if '?' in self._id:
                self._id = self._id.split('?')[0]
        else:
            self._id = id

    def __repr__(self):
        return '<Message id:{id} ttl:{ttl}>'.format(id=self._id,
                                                    ttl=self.ttl)

    @property
    def claim_id(self):
        if '=' in self.href:
            return self.href.split('=')[-1]

    def delete(self):
        req, trans = self.queue.client._request_and_transport()
        core.message_delete(trans, req, self.queue._name,
                            self._id, self.claim_id)


def create_object(parent):
    return lambda args: Message(parent, **args)
