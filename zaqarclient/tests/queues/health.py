# Copyright (c) 2016 Catalyst IT Ltd.
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


class QueuesV2HealthUnitTest(base.QueuesTestBase):

    def test_health(self):
        expect_health = {u'catalog_reachable': True,
                         u'redis': {u'operation_status': {},
                                    u'storage_reachable': True}
                         }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            health_content = json.dumps(expect_health)
            health_resp = response.Response(None, health_content)
            send_method.side_effect = iter([health_resp])

            health = self.client.health()
            self.assertEqual(expect_health, health)


class QueuesV2HealthFunctionalTest(base.QueuesTestBase):
    def test_ping(self):
        # NOTE(flwang): If test env is not pingable, then the test should fail
        self.assertTrue(self.client.ping())

    def test_health(self):
        health = self.client.health()
        # NOTE(flwang): If everything is ok, then zaqar server will return a
        # JSON(dict).
        self.assertIsInstance(health, dict)
