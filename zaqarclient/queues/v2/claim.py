# Copyright (c) 2014 Rackspace, Inc.
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

from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import iterator
from zaqarclient.queues.v2 import message


class Claim(object):
    def __init__(self, queue, id=None,
                 ttl=None, grace=None, limit=None):
        self._queue = queue
        self.id = id
        self._ttl = ttl
        self._grace = grace
        self._age = None
        self._limit = limit
        self._message_iter = None
        if id is None:
            self._create()

    def __repr__(self):
        return '<Claim id:{id} ttl:{ttl} age:{age}>'.format(id=self.id,
                                                            ttl=self.ttl,
                                                            age=self.age)

    def _get(self):
        req, trans = self._queue.client._request_and_transport()

        claim_res = core.claim_get(trans, req, self._queue._name,
                                   self.id)
        self._age = claim_res['age']
        self._ttl = claim_res['ttl']
        self._grace = claim_res.get('grace')
        msgs = claim_res.get('messages', [])
        self._message_iter = iterator._Iterator(self._queue.client,
                                                msgs,
                                                'messages',
                                                message.create_object(
                                                    self._queue
                                                ))

    def _create(self):
        req, trans = self._queue.client._request_and_transport()
        msgs = core.claim_create(trans, req,
                                 self._queue._name,
                                 ttl=self._ttl,
                                 grace=self._grace,
                                 limit=self._limit)

        # extract the id from the first message
        if msgs is not None:
            msgs = msgs['messages']
            self.id = msgs[0]['href'].split('=')[-1]

        self._message_iter = iterator._Iterator(self._queue.client,
                                                msgs or [],
                                                'messages',
                                                message.create_object(
                                                    self._queue
                                                ))

    def __iter__(self):
        if self._message_iter is None:
            self._get()
        return self._message_iter

    @property
    def age(self):
        self._get()
        return self._age

    @property
    def ttl(self):
        if self._ttl is None:
            self._get()
        return self._ttl

    def delete(self):
        req, trans = self._queue.client._request_and_transport()
        core.claim_delete(trans, req, self._queue._name, self.id)

    def update(self, ttl=None, grace=None):
        req, trans = self._queue.client._request_and_transport()
        kwargs = {}
        if ttl is not None:
            kwargs['ttl'] = ttl
        if grace is not None:
            kwargs['grace'] = grace
        res = core.claim_update(trans, req, self._queue._name, self.id,
                                **kwargs)
        # if the update succeeds, update our attributes.
        if ttl is not None:
            self._ttl = ttl
        if grace is not None:
            self._grace = grace
        return res
