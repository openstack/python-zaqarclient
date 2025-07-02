# Copyright (c) 2014 Rackspace Hosting.
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
import time
from unittest import mock

from zaqarclient.queues.v2 import claim
from zaqarclient.tests.queues import base
from zaqarclient.transport import errors
from zaqarclient.transport import response


class QueueV2ClaimUnitTest(base.QueuesTestBase):

    def test_claim(self):
        result = [{
            'href': '/v2/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }, {
            'href': '/v2/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b02',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }]

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps({'messages': result}))
            send_method.return_value = resp

            claimed = self.queue.claim(ttl=60, grace=60)
            # messages doesn't support len()
            num_tested = 0
            for num, msg in enumerate(claimed):
                num_tested += 1
                self.assertEqual(result[num]['href'], msg.href)
            self.assertEqual(len(result), num_tested)

    def test_claim_limit(self):
        def verify_limit(request):
            self.assertIn('limit', request.params)
            self.assertEqual(10, request.params['limit'])
            # NOTE(flaper87): We don't care about the response here,
            # fake it.
            return response.Response(None, "{0: [], 'messages': []}")

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            send_method.side_effect = verify_limit
            self.queue.claim(ttl=60, grace=60, limit=10)

    def test_claim_get_by_id(self):
        result = {
            'href': '/v2/queues/fizbit/messages/50b68a50d6cb01?claim_id=4524',
            'age': 790,
            'ttl': 800,
            'messages': [{
                'href': '/v2/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
                'ttl': 800,
                'age': 790,
                'body': {'event': 'ActivateAccount', 'mode': 'active'}
            }]}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(result))
            send_method.return_value = resp

            cl = self.queue.claim(id='5245432')
            # messages doesn't support len()
            num_tested = 0
            for num, msg in enumerate(cl):
                num_tested += 1
                self.assertEqual(result['messages'][num]['href'], msg.href)
            self.assertEqual(len(result['messages']), num_tested)

    def test_claim_update(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.claim(id='5245432').update(ttl=444, grace=987)

            # NOTE(asalkeld): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_claim_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.claim(id='4225').delete()

            # NOTE(asalkeld): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV2ClaimFunctionalTest(base.QueuesTestBase):

    def test_message_claim_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [{'ttl': 60, 'body': 'Post It 1!'}]
        queue.post(messages)

        messages = queue.claim(ttl=120, grace=120)
        self.assertIsInstance(messages, claim.Claim)
        self.assertGreaterEqual(len(list(messages)), 0)

    def test_claim_get_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        res = queue.claim(ttl=100, grace=100)
        claim_id = res.id
        cl = queue.claim(id=claim_id)
        self.assertEqual(claim_id, cl.id)

    def test_claim_create_delete_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [{'ttl': 60, 'body': 'Post It 1!'}]
        queue.post(messages)

        cl = queue.claim(ttl=120, grace=120)
        claim_id = cl.id
        cl.delete()
        self.assertRaises(errors.ResourceNotFound, queue.claim, id=claim_id)

    def test_claim_age(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [{'ttl': 60, 'body': 'image.upload'}]
        queue.post(messages)

        res = queue.claim(ttl=100, grace=60)
        self.assertGreaterEqual(res.age, 0)
        time.sleep(2)
        self.assertGreaterEqual(res.age, 2)
