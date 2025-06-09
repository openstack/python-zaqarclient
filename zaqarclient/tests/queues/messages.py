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

import json
from unittest import mock

from zaqarclient.tests.queues import base
from zaqarclient.transport import response


class QueuesV1MessageUnitTest(base.QueuesTestBase):

    def test_message_delete(self):
        returned = {
            'href': '/v2/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            msg = self.queue.message('50b68a50d6f5b8c8a7c62b01')

            send_method.return_value = None
            self.assertIsNone(msg.delete())

    def test_message_delete_with_claim(self):
        returned = {
            'href': '/v2/queues/fizbit/messages/50b68a50d6?claim_id=5388b5dd0',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            msg = self.queue.message('50b68a50d6')

            send_method.return_value = None
            self.assertIsNone(msg.delete())


class QueuesV2MessageUnitTest(QueuesV1MessageUnitTest):

    def test_message_delete_with_claim(self):
        pass

    def test_message_delete(self):
        pass
