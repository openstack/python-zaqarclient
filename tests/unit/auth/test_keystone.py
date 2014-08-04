# Copyright (c) 2013  Red Hat, Inc.
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

try:
    from keystoneclient.v2_0 import client as ksclient
except ImportError:
    ksclient = None

from zaqarclient import auth
from zaqarclient.tests import base
from zaqarclient.transport import request


class _FakeKeystoneClient(object):
    auth_token = 'test-token'

    def __init__(self, *args, **kwargs):
        pass


class TestKeystoneAuth(base.TestBase):

    def setUp(self):
        super(TestKeystoneAuth, self).setUp()

        if not ksclient:
            self.skipTest('Keystone client is not installed')

        self.auth = auth.get_backend(backend='keystone',
                                     options=self.conf)

    def test_no_token(self):
        test_endpoint = 'http://example.org:8888'

        with mock.patch.object(ksclient, 'Client',
                               new_callable=lambda: _FakeKeystoneClient):

            with mock.patch.object(self.auth, '_get_endpoint') as get_endpoint:
                get_endpoint.return_value = test_endpoint

                req = self.auth.authenticate(1, request.Request())
                self.assertEqual(req.endpoint, test_endpoint)
                self.assertIn('X-Auth-Token', req.headers)

    def test_with_token(self):
        self.config(os_auth_token='test-token')
        req = request.Request(endpoint='http://example.org:8888')
        req = self.auth.authenticate(1, req)
        self.assertIn('X-Auth-Token', req.headers)
        self.assertIn(req.headers['X-Auth-Token'], 'test-token')
