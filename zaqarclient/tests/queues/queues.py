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

from zaqarclient import errors
from zaqarclient.queues import client
from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v1 import message
from zaqarclient.queues.v2 import subscription
from zaqarclient.tests.queues import base
from zaqarclient.transport import response


class QueuesV1QueueUnitTest(base.QueuesTestBase):

    def test_queue_metadata(self):
        test_metadata = {'type': 'Bank Accounts'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp

            metadata = self.queue.metadata(test_metadata)
            self.assertEqual(test_metadata, metadata)

    def test_queue_metadata_update(self):
        test_metadata = {'type': 'Bank Accounts'}
        new_meta = {'flavor': 'test'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp

            metadata = self.queue.metadata(test_metadata)
            self.assertEqual(test_metadata, metadata)

            metadata = self.queue.metadata(new_meta)
            self.assertEqual(new_meta, metadata)

    def test_queue_create(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.ensure_exists()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_valid_name(self):
        self.assertRaises(ValueError, self.client.queue, "")

    def test_queue_valid_name_with_pound(self):
        self.assertRaises(ValueError, self.client.queue, "123#456")

    def test_queue_valid_name_with_percent(self):
        self.assertRaises(ValueError, self.client.queue, "123%456")

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

    def test_message_delete_many(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            rst = self.queue.delete_messages('50b68a50d6f5b8c8a7c62b01',
                                             '50b68a50d6f5b8c8a7c62b02')
            self.assertIsNone(rst)

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1QueueFunctionalTest(base.QueuesTestBase):

    def test_queue_create_functional(self):
        queue = self.client.queue("nonono")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertTrue(queue.exists())

    def test_queue_delete_functional(self):
        queue = self.client.queue("nonono")
        self.addCleanup(queue.delete)
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
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)
        queue.post(messages)
        stats = queue.stats
        self.assertEqual(3, stats["messages"]["free"])

    def test_queue_metadata_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Clear metadata's cache
        queue._metadata = None
        metadata = queue.metadata()
        self.assertEqual(test_metadata['type'], metadata['type'])

    def test_queue_metadata_reload_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Overwrite the cached value
        # but don't clear it.
        queue._metadata = 'test'
        metadata = queue.metadata(force_reload=True)
        self.assertEqual(test_metadata['type'], metadata['type'])

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
        self.assertEqual(3, len(result['resources']))

    def test_message_list_functional(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [{'ttl': 60, 'body': 'Post It 1!'}]
        queue.post(messages)

        messages = queue.messages()
        self.assertIsInstance(messages, iterator._Iterator)
        self.assertGreaterEqual(len(list(messages)), 0)

    def test_message_list_echo_functional(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]
        queue.post(messages)
        messages = queue.messages(echo=True)
        self.assertIsInstance(messages, iterator._Iterator)
        self.assertGreaterEqual(len(list(messages)), 3)

    def test_message_get_functional(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]

        res = queue.post(messages)['resources']
        msg_id = res[0].split('/')[-1]
        msg = queue.message(msg_id)
        self.assertIsInstance(msg, message.Message)
        self.assertEqual(res[0], msg.href)

    def test_message_get_many_functional(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]

        res = queue.post(messages)['resources']
        msgs_id = [ref.split('/')[-1] for ref in res]
        messages = queue.messages(*msgs_id)
        self.assertIsInstance(messages, iterator._Iterator)
        messages = list(messages)
        length = len(messages)
        if length == 3:
            bodies = set(message.body for message in messages)
            self.assertEqual(
                set(['Post It 1!', 'Post It 2!', 'Post It 3!']), bodies)
        elif length == 1:
            # FIXME(therve): Old broken behavior, remove it as some point
            pass
        else:
            self.fail("Wrong number of messages: '%d'" % length)

    def test_message_delete_many_functional(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
        ]

        res = queue.post(messages)['resources']
        msgs_id = [ref.split('/')[-1] for ref in res]
        queue.delete_messages(*msgs_id)

        messages = queue.messages()
        self.assertEqual(0, len(list(messages)))


class QueuesV1_1QueueUnitTest(QueuesV1QueueUnitTest):

    def test_message_pop(self):
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

            msg = self.queue.pop(count=2)
            self.assertIsInstance(msg, iterator._Iterator)

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_metadata(self):
        test_metadata = {'type': 'Bank Accounts'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp
            self.assertRaises(RuntimeError, self.queue.metadata, test_metadata)

    def test_queue_metadata_update(self):
        # v1.1 doesn't support set queue metadata
        pass


class QueuesV1_1QueueFunctionalTest(QueuesV1QueueFunctionalTest):

    def test_queue_create_functional(self):
        pass

    def test_queue_exists_functional(self):
        queue = self.client.queue("404")
        self.assertRaises(errors.InvalidOperation, queue.exists)

    def test_queue_delete_functional(self):
        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 3!'},
        ]

        queue.post(messages)
        queue.delete()
        self.assertEqual(0, len(list(queue.messages(echo=True))))

    def test_message_pop(self):
        queue = self.client.queue("test_queue")
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        messages = [
            {'ttl': 60, 'body': 'Post It 1!'},
            {'ttl': 60, 'body': 'Post It 2!'},
            {'ttl': 60, 'body': 'Post It 2!'},
        ]

        queue.post(messages)
        messages = queue.pop(count=2)
        self.assertIsInstance(messages, iterator._Iterator)
        self.assertEqual(2, len(list(messages)))

        remaining = queue.messages(echo=True)
        self.assertEqual(1, len(list(remaining)))

    def test_queue_metadata_functional(self):
        # v1.1 doesn't support set queue metadata
        pass

    def test_queue_metadata_reload_functional(self):
        # v1.1 doesn't support set queue metadata
        pass


class QueuesV2QueueUnitTest(QueuesV1_1QueueUnitTest):

    def test_message_get(self):
        pass

    def test_queue_subscriptions(self):
        result = {
            "subscriptions": [{
                "source": 'test',
                "id": "1",
                "subscriber": 'http://trigger.me',
                "ttl": 3600,
                "age": 1800,
                "confirmed": False,
                "options": {}},
                {
                "source": 'test',
                "id": "2",
                "subscriber": 'http://trigger.you',
                "ttl": 7200,
                "age": 1800,
                "confirmed": False,
                "options": {}}]
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(result))
            send_method.return_value = resp

            subscriptions = self.queue.subscriptions()
            subscriber_list = [s.subscriber for s in list(subscriptions)]
            self.assertIn('http://trigger.me', subscriber_list)
            self.assertIn('http://trigger.you', subscriber_list)

    def test_queue_metadata(self):
        # checked in "test_queue_metadata_update"
        pass

    def test_queue_metadata_update(self):
        test_metadata = {'type': 'Bank Accounts', 'name': 'test1'}
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp

            # add 'test_metadata'
            metadata = self.queue.metadata(new_meta=test_metadata)
            self.assertEqual(test_metadata, metadata)

        new_metadata_replace = {'type': 'test', 'name': 'test1'}
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(new_metadata_replace))
            send_method.return_value = resp
            # repalce 'type'
            metadata = self.queue.metadata(
                new_meta=new_metadata_replace)
            expect_metadata = {'type': 'test', "name": 'test1'}
            self.assertEqual(expect_metadata, metadata)

        remove_metadata = {'name': 'test1'}
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(remove_metadata))
            send_method.return_value = resp
            # remove 'type'
            metadata = self.queue.metadata(new_meta=remove_metadata)
            expect_metadata = {"name": 'test1'}
            self.assertEqual(expect_metadata, metadata)

    def test_queue_purge(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.purge()

            # NOTE(flwang): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_purge_messages(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.purge(resource_types=['messages'])
            self.assertEqual({"resource_types": ["messages"]},
                             json.loads(send_method.call_args[0][0].content))


class QueuesV2QueueFunctionalTest(QueuesV1_1QueueFunctionalTest):

    def test_signed_url(self):
        queue = self.client.queue('test_queue')
        messages = [{'ttl': 300, 'body': 'Post It!'}]
        queue.post(messages)
        self.addCleanup(queue.delete)
        signature = queue.signed_url()
        opts = {
            'paths': signature['paths'],
            'expires': signature['expires'],
            'methods': signature['methods'],
            'signature': signature['signature'],
            'os_project_id': signature['project'],
        }
        auth_opts = {'backend': 'signed-url',
                     'options': opts}
        conf = {'auth_opts': auth_opts}
        signed_client = client.Client(self.url, self.version, conf)
        queue = signed_client.queue('test_queue')
        [message] = list(queue.messages())
        self.assertEqual('Post It!', message.body)

    def test_queue_subscriptions(self):
        queue_name = 'test_queue'
        queue = self.client.queue(queue_name, force_create=True)
        self.addCleanup(queue.delete)
        queue._get_transport = mock.Mock(return_value=self.transport)

        subscription.Subscription(self.client, queue_name,
                                  subscriber='http://trigger.me')
        subscription.Subscription(self.client, queue_name,
                                  subscriber='http://trigger.you')

        get_subscriptions = queue.subscriptions()
        self.assertIsInstance(get_subscriptions, iterator._Iterator)
        self.assertEqual(2, len(list(get_subscriptions)))

    def test_queue_metadata_reload_functional(self):
        test_metadata = {'type': 'Bank Accounts', 'name': 'test1'}
        queue = self.client.queue("meta-test", force_create=True)
        self.addCleanup(queue.delete)

        queue.metadata(new_meta=test_metadata)
        # NOTE(flaper87): Overwrite the cached value
        # but don't clear it.
        queue._metadata = 'test'
        expect_metadata = {'type': 'Bank Accounts', 'name': 'test1',
                           '_max_messages_post_size': 262144,
                           '_default_message_ttl': 3600,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None}
        metadata = queue.metadata(force_reload=True)
        self.assertEqual(expect_metadata, metadata)

    def test_queue_metadata_functional(self):
        queue = self.client.queue("meta-test", force_create=True)
        self.addCleanup(queue.delete)
        # add two metadatas
        test_metadata = {'type': 'Bank Accounts', 'name': 'test1'}
        queue.metadata(new_meta=test_metadata)
        # NOTE(flaper87): Clear metadata's cache
        queue._metadata = None
        metadata = queue.metadata()
        expect_metadata = {'type': 'Bank Accounts', 'name': 'test1',
                           '_max_messages_post_size': 262144,
                           '_default_message_ttl': 3600,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None}
        self.assertEqual(expect_metadata, metadata)

        # replace 'type', '_default_message_ttl' and add a new one 'age'
        replace_add_metadata = {'type': 'test', 'name': 'test1', 'age': 13,
                                '_default_message_ttl': 1000}
        queue.metadata(new_meta=replace_add_metadata)
        queue._metadata = None
        metadata = queue.metadata()
        expect_metadata = {'type': 'test', 'name': 'test1', 'age': 13,
                           '_max_messages_post_size': 262144,
                           '_default_message_ttl': 1000,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None}
        self.assertEqual(expect_metadata, metadata)

        # replace 'name', remove 'type', '_default_message_ttl' and add a new
        # one 'fake'.
        replace_remove_add_metadata = {'name': 'test2',
                                       'age': 13,
                                       'fake': 'test_fake',
                                       }
        queue.metadata(new_meta=replace_remove_add_metadata)
        queue._metadata = None
        metadata = queue.metadata()
        expect_metadata = {'name': 'test2', 'age': 13, 'fake': 'test_fake',
                           '_max_messages_post_size': 262144,
                           '_default_message_ttl': 3600,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None}
        self.assertEqual(expect_metadata, metadata)

        # replace 'name' to empty string and add a new empty dict 'empty_dict'.
        replace_add_metadata = {'name': '',
                                'age': 13,
                                'fake': 'test_fake',
                                'empty_dict': {}
                                }
        queue.metadata(new_meta=replace_add_metadata)
        queue._metadata = None
        metadata = queue.metadata()
        expect_metadata = {'name': '', 'age': 13, 'fake': 'test_fake',
                           '_max_messages_post_size': 262144,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None,
                           '_default_message_ttl': 3600, 'empty_dict': {}}
        self.assertEqual(expect_metadata, metadata)

        # Delete all metadata.
        remove_all = {}
        queue.metadata(new_meta=remove_all)
        queue._metadata = None
        metadata = queue.metadata()
        expect_metadata = {'_max_messages_post_size': 262144,
                           '_default_message_ttl': 3600,
                           '_default_message_delay': 0,
                           '_dead_letter_queue': None,
                           '_dead_letter_queue_messages_ttl': None,
                           '_max_claim_count': None}
        self.assertEqual(expect_metadata, metadata)
