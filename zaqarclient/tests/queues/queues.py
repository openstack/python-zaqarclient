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
import mock

from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v1 import message
from zaqarclient.tests.queues import base
from zaqarclient.transport import response


class QueuesV1QueueUnitTest(base.QueuesTestBase):

    def test_queue_metadata(self):
        test_metadata = {'type': 'Bank Accounts'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp

            metadata = self.queue.metadata()
            self.assertEqual(metadata, test_metadata)

    def test_queue_create(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.ensure_exists()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.delete()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_exists(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.exists()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_stats(self):
        result = {
            "messages": {
                "free": 146929,
                "claimed": 2409,
                "total": 149338,
                "oldest": {
                    "href": "/v1/queues/qq/messages/50b68a50d6f5b8c8a7c62b01",
                    "age": 63,
                    "created": "2013-08-12T20:44:55Z"
                },
                "newest": {
                    "href": "/v1/queues/qq/messages/50b68a50d6f5b8c8a7c62b01",
                    "age": 12,
                    "created": "2013-08-12T20:45:46Z"
                }
            }
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(result))
            send_method.return_value = resp

            stats = self.queue.stats
            self.assertEqual(result, stats)

    def test_message_post(self):
        messages = [{'ttl': 30, 'body': 'Post It!'}]

        result = {
            "resources": [
                "/v1/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01"
            ],
            "partial": False
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(result))
            send_method.return_value = resp

            posted = self.queue.post(messages)
            self.assertEqual(result, posted)

    def test_message_list(self):
        returned = {
            'links': [{
                'rel': 'next',
                'href': '/v1/queues/fizbit/messages?marker=6244-244224-783'
            }],
            'messages': [{
                'href': '/v1/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
                'ttl': 800,
                'age': 790,
                'body': {'event': 'ActivateAccount',
                         'mode': 'active'}
            }]
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            msgs = self.queue.messages(limit=1)
            self.assertIsInstance(msgs, iterator._Iterator)

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_message_get(self):
        returned = {
            'href': '/v1/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            msgs = self.queue.message('50b68a50d6f5b8c8a7c62b01')
            self.assertIsInstance(msgs, message.Message)

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_message_get_many(self):
        returned = [{
            'href': '/v1/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b01',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }, {
            'href': '/v1/queues/fizbit/messages/50b68a50d6f5b8c8a7c62b02',
            'ttl': 800,
            'age': 790,
            'body': {'event': 'ActivateAccount', 'mode': 'active'}
        }]

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            msg = self.queue.messages('50b68a50d6f5b8c8a7c62b01',
                                      '50b68a50d6f5b8c8a7c62b02')
            self.assertIsInstance(msg, iterator._Iterator)

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1QueueFunctionalTest(base.QueuesTestBase):

    def test_queue_create_functional(self):
        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertTrue(queue.exists())

    def test_queue_delete_functional(self):
        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertTrue(queue.exists())
        queue.delete()
        self.assertFalse(queue.exists())

    def test_queue_exists_functional(self):
        queue = self.client.queue("404", auto_create=False)
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertFalse(queue.exists())

    def test_queue_stats_functional(self):
        messages = [
            {'ttl': 60, 'body': 'Post It!'},
            {'ttl': 60, 'body': 'Post It!'},
            {'ttl': 60, 'body': 'Post It!'},
        ]

        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        queue.post(messages)
        stats = queue.stats
        self.assertEqual(stats["messages"]["free"], 3)

    def test_queue_metadata_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Clear metadata's cache
        queue._metadata = None
        metadata = queue.metadata()
        self.assertEqual(metadata, test_metadata)

    def test_queue_metadata_reload_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Overwrite the cached value
        # but don't clear it.
        queue._metadata = 'test'
        metadata = queue.metadata(force_reload=True)
        self.assertEqual(metadata, test_metadata)

    def test_message_post_functional(self):
        messages = [
            {'ttl': 60, 'body': 'Post It!'},
            {'ttl': 60, 'body': 'Post It!'},
            {'ttl': 60, 'body': 'Post It!'},
        ]

        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        result = queue.post(messages)
        self.assertIn('resources', result)
        self.assertEqual(len(result['resources']), 3)

    def test_message_list_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [{'ttl': 60, 'body': 'Post It 1!'}]
        queue.post(messages)

        messages = queue.messages()
        self.assertTrue(isinstance(messages, iterator._Iterator))
        self.assertGreaterEqual(len(list(messages)), 0)

    def test_message_list_echo_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]
        queue.post(messages)
        messages = queue.messages(echo=True)
        self.assertTrue(isinstance(messages, iterator._Iterator))
        self.assertGreaterEqual(len(list(messages)), 3)

    def test_message_get_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]

        res = queue.post(messages)['resources']
        msg_id = res[0].split('/')[-1]
        msg = queue.message(msg_id)
        self.assertTrue(isinstance(msg, message.Message))
        self.assertEqual(msg.href, res[0])

    def test_message_get_many_functional(self):
        queue = self.client.queue("test_queue")
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},

            # NOTE(falper87): Waiting for
            # https://github.com/racker/falcon/issues/198
            #{'ttl': 60, 'body': 'Post It 2!'},
            #{'ttl': 60, 'body': 'Post It 3!'},
        ]

        res = queue.post(messages)['resources']
        msgs_id = [ref.split('/')[-1] for ref in res]
        messages = queue.messages(*msgs_id)
        self.assertTrue(isinstance(messages, iterator._Iterator))
        self.assertEqual(len(list(messages)), 1)
