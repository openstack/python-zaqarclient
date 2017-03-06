# Copyright (c) 2015 Catalyst IT Ltd.
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

from zaqarclient.tests.queues import base
from zaqarclient.transport import errors
from zaqarclient.transport import response


class QueuesV2SubscriptionUnitTest(base.QueuesTestBase):

    def test_subscription_create(self):
        subscription_data = {'subscriber': 'http://trigger.me',
                             'ttl': 3600}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            create_resp = response.Response(None,
                                            '{"subscription_id": "fake_id"}')
            get_content = ('{"subscriber": "http://trigger.me","ttl": 3600, '
                           '"id": "fake_id"}')
            get_resp = response.Response(None, get_content)
            send_method.side_effect = iter([create_resp, get_resp])

            # NOTE(flwang): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            subscription = self.client.subscription('beijing',
                                                    **subscription_data)
            self.assertEqual('http://trigger.me', subscription.subscriber)
            self.assertEqual(3600, subscription.ttl)
            self.assertEqual('fake_id', subscription.id)

    def test_subscription_create_duplicate_throws_conflicterror(self):
        subscription_data = {'subscriber': 'http://trigger.me',
                             'ttl': 3600}

        with mock.patch.object(self.transport.client, 'request',
                               autospec=True) as request_method:

            class FakeRawResponse(object):
                def __init__(self):
                    self.text = ''
                    self.headers = {}
                    self.status_code = 409
            request_method.return_value = FakeRawResponse()

            self.assertRaises(errors.ConflictError, self.client.subscription,
                              'beijing', **subscription_data)

    def test_subscription_update(self):
        subscription_data = {'subscriber': 'http://trigger.me',
                             'ttl': 3600}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            create_resp = response.Response(None,
                                            '{"subscription_id": "fake_id"}')
            get_content = ('{"subscriber": "http://trigger.me","ttl": 3600, '
                           '"id": "fake_id"}')
            get_resp = response.Response(None, get_content)
            update_content = json.dumps({'subscriber': 'fake_subscriber'})
            update_resp = response.Response(None, update_content)
            send_method.side_effect = iter([create_resp, get_resp,
                                            update_resp])

            # NOTE(flwang): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            subscription = self.client.subscription('beijing',
                                                    **subscription_data)

            subscription.update({'subscriber': 'fake_subscriber'})
            self.assertEqual('fake_subscriber', subscription.subscriber)

    def test_subscription_delete(self):
        subscription_data = {'subscriber': 'http://trigger.me',
                             'ttl': 3600}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            create_resp = response.Response(None,
                                            '{"subscription_id": "fake_id"}')
            get_content = ('{"subscriber": "http://trigger.me","ttl": 3600, '
                           '"id": "fake_id"}')
            get_resp = response.Response(None, get_content)
            send_method.side_effect = iter([create_resp, get_resp, None,
                                            errors.ResourceNotFound])

            # NOTE(flwang): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            subscription = self.client.subscription('beijing',
                                                    **subscription_data)
            self.assertEqual('http://trigger.me', subscription.subscriber)
            self.assertEqual(3600, subscription.ttl)
            self.assertEqual('fake_id', subscription.id)

            subscription.delete()
            self.assertRaises(errors.ResourceNotFound,
                              self.client.subscription,
                              'beijing', **{'id': 'fake_id'})

    def test_subscription_get(self):
        subscription_data = {'subscriber': 'http://trigger.me',
                             'ttl': 3600}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(subscription_data))
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            kwargs = {'id': 'fake_id'}
            subscription = self.client.subscription('test', **kwargs)
            self.assertEqual('http://trigger.me', subscription.subscriber)
            self.assertEqual(3600, subscription.ttl)

    def test_subscription_list(self):
        subscription_data = {'subscriptions':
                             [{'source': 'beijing',
                               'id': '568afabb508f153573f6a56f',
                               'subscriber': 'http://trigger.me',
                               'ttl': 3600,
                               'age': 1800,
                               'confirmed': False,
                               'options': {}},
                              {'source': 'beijing',
                               'id': '568afabb508f153573f6a56x',
                               'subscriber': 'http://trigger.you',
                               'ttl': 7200,
                               'age': 2309,
                               'confirmed': True,
                               'options': {'oh stop': 'triggering'}}]}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            list_resp = response.Response(None,
                                          json.dumps(subscription_data))
            send_method.side_effect = iter([list_resp])

            # NOTE(flwang): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            subscriptions = list(self.client.subscriptions('beijing'))
            self.assertEqual(2, len(subscriptions))

            subscriber_list = [s.subscriber for s in subscriptions]
            self.assertIn('http://trigger.me', subscriber_list)
            self.assertIn('http://trigger.you', subscriber_list)

            # Let's pick one of the subscriptions and check all of its fields
            for sub in subscriptions:
                if sub.subscriber == 'http://trigger.you':
                    self.assertEqual('beijing', sub.queue_name)
                    self.assertEqual('568afabb508f153573f6a56x', sub.id)
                    self.assertEqual(7200, sub.ttl)
                    self.assertEqual({'oh stop': 'triggering'}, sub.options)


class QueuesV2SubscriptionFunctionalTest(base.QueuesTestBase):

    def setUp(self):
        super(QueuesV2SubscriptionFunctionalTest, self).setUp()

        self.queue_name = 'beijing'
        queue = self.client.queue(self.queue_name, force_create=True)
        self.addCleanup(queue.delete)

        subscription_data_1 = {'subscriber': 'http://trigger.me', 'ttl': 3600}
        subscription_data_2 = {'subscriber': 'http://trigger.he', 'ttl':
                               7200, 'options': {'check everything': True}}
        self.subscription_1 = self.client.subscription(self.queue_name,
                                                       **subscription_data_1)
        self.addCleanup(self.subscription_1.delete)

        self.subscription_2 = self.client.subscription(self.queue_name,
                                                       **subscription_data_2)
        self.addCleanup(self.subscription_2.delete)

    def test_subscription_create(self):
        self.assertEqual('http://trigger.me', self.subscription_1.subscriber)
        self.assertEqual(3600, self.subscription_1.ttl)

        self.assertEqual('http://trigger.he', self.subscription_2.subscriber)
        self.assertEqual(7200, self.subscription_2.ttl)

    def test_subscription_create_duplicate(self):
        subscription_data_2 = {'subscriber': 'http://trigger.he', 'ttl':
                               7200, 'options': {'check everything': True}}
        # Now Zaqar support subscription confirm, when users try to recreate a
        # subscription which is already created and not confirmed, Zaqar will
        # try to reconfirm this subscription and return 201 instead of 409.
        new_subscription = self.client.subscription('beijing',
                                                    **subscription_data_2)
        self.assertEqual(new_subscription.id, self.subscription_2.id)

    def test_subscription_update(self):
        sub = self.client.subscription(self.queue_name, auto_create=False,
                                       **{'id': self.subscription_1.id})
        data = {'subscriber': 'http://trigger.ok', 'ttl': 1000}
        sub.update(data)
        self.assertEqual('http://trigger.ok', sub.subscriber)
        self.assertEqual(1000, sub.ttl)

    def test_subscription_delete(self):
        self.subscription_1.delete()

        subscription_data = {'id': self.subscription_1.id}
        self.assertRaises(errors.ResourceNotFound, self.client.subscription,
                          self.queue_name, **subscription_data)

    def test_subscription_get(self):
        kwargs = {'id': self.subscription_1.id}
        subscription_get = self.client.subscription(self.queue_name, **kwargs)

        self.assertEqual('http://trigger.me', subscription_get.subscriber)
        self.assertEqual(3600, subscription_get.ttl)

    def test_subscription_list(self):
        subscriptions = self.client.subscriptions(self.queue_name)
        subscriptions = list(subscriptions)
        self.assertEqual(2, len(subscriptions))

        subscriber_list = [s.subscriber for s in subscriptions]
        self.assertIn('http://trigger.me', subscriber_list)
        self.assertIn('http://trigger.he', subscriber_list)

        # Let's pick one of the subscriptions and check all of its fields
        for sub in subscriptions:
            if sub.subscriber == 'http://trigger.he':
                self.assertEqual('beijing', sub.queue_name)
                self.assertEqual(self.subscription_2.id, sub.id)
                self.assertEqual(7200, sub.ttl)
                self.assertEqual({'check everything': True}, sub.options)
