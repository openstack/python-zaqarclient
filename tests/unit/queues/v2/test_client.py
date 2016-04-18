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
from zaqarclient.tests.queues import base
from zaqarclient.transport import errors
from zaqarclient.transport import http

VERSIONS = [2]


@ddt.ddt
class TestClient(base.QueuesTestBase):
    transport_cls = http.HttpTransport
    url = 'http://127.0.0.1:8888/v2'
    version = VERSIONS[0]

    @ddt.data(*VERSIONS)
    def test_transport(self, version):
        cli = client.Client('http://example.com',
                            version, {"auth_opts": {'backend': 'noauth'}})
        self.assertIsNotNone(cli.transport())

    @ddt.data(*VERSIONS)
    def test_ping_ok(self, version):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.return_value = None
            self.assertTrue(self.client.ping())

    @ddt.data(*VERSIONS)
    def test_ping_bad(self, version):
        def raise_error(*args, **kwargs):
            raise errors.ServiceUnavailableError()

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.side_effect = raise_error
            self.assertFalse(self.client.ping())
