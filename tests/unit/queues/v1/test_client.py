# Copyright 2014 IBM Corp.
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

from zaqarclient.queues import client
from zaqarclient.queues.v1 import core
from zaqarclient.tests import base
from zaqarclient.transport import response

VERSION = 1


class TestClient(base.TestBase):

    def test_transport(self):
        cli = client.Client('http://example.com',
                            VERSION, {})
        self.assertIsNotNone(cli.transport())

    def test_health(self):
        cli = client.Client('http://example.com',
                            VERSION, {})
        with mock.patch.object(core, 'health', autospec=True) as core_health:
            resp = response.Response(None, None)
            core_health.return_value = resp
            self.assertIsNotNone(cli.health())
