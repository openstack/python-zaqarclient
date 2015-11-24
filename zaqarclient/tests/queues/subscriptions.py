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

import mock

from zaqarclient.tests.queues import base
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


class QueuesV2SubscriptionFunctionalTest(base.QueuesTestBase):

    def setUp(self):
        super(QueuesV2SubscriptionFunctionalTest, self).setUp()

        # TODO(flwang): Now there is a bug(#1529168) for the subscription TTL,
        # so we will add a test case for TTL after the bug fixed.
        self.queue_name = 'beijing'
        queue = self.client.queue(self.queue_name, force_create=True)
        self.addCleanup(queue.delete)

        subscription_data_1 = {'subscriber': 'http://trigger.me', 'ttl': 3600}
        subscription_data_2 = {'subscriber': 'http://trigger.he', 'ttl': 7200}
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
