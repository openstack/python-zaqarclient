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

from zaqarclient.queues.v1 import claim
from zaqarclient.queues.v1 import iterator as iterate
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import message


class Claim(claim.Claim):

    def _create(self):
        req, trans = self._queue.client._request_and_transport()
        msgs = core.claim_create(trans, req,
                                 self._queue._name,
                                 ttl=self._ttl,
                                 grace=self._grace,
                                 limit=self._limit)

        # extract the id from the first message
        if msgs is not None:
            if self._queue.client.api_version >= 1.1:
                msgs = msgs['messages']
            self.id = msgs[0]['href'].split('=')[-1]

        self._message_iter = iterate._Iterator(self._queue.client,
                                               msgs or [],
                                               'messages',
                                               message.create_object(
                                                   self._queue
                                               ))
