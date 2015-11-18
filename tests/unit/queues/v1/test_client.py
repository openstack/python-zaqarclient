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

import ddt

from zaqarclient.queues import client
from zaqarclient.queues.v1 import core
from zaqarclient.tests import base
from zaqarclient.transport import errors

VERSIONS = [1, 1.1]


@ddt.ddt
class TestClient(base.TestBase):

    @ddt.data(*VERSIONS)
    def test_transport(self, version):
        cli = client.Client('http://example.com',
                            version, {"auth_opts": {'backend': 'noauth'}})
        self.assertIsNotNone(cli.transport())

    @ddt.data(*VERSIONS)
    def test_health_ok(self, version):
        cli = client.Client('http://example.com',
                            version, {"auth_opts": {'backend': 'noauth'}})
        with mock.patch.object(core, 'health', autospec=True) as core_health:
            core_health.return_value = None
            self.assertTrue(cli.health())

    @ddt.data(*VERSIONS)
    def test_health_bad(self, version):
        cli = client.Client('http://example.com',
                            version, {"auth_opts": {'backend': 'noauth'}})

        def raise_error(*args, **kwargs):
            raise errors.ServiceUnavailableError()

        with mock.patch.object(core, 'health', autospec=True) as core_health:
            core_health.side_effect = raise_error
            self.assertFalse(cli.health())
