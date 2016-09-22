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

from keystoneauth1 import session

from zaqarclient import auth
from zaqarclient.tests import base
from zaqarclient.transport import request


class TestKeystoneAuth(base.TestBase):

    def setUp(self):
        super(TestKeystoneAuth, self).setUp()

        self.auth = auth.get_backend(options=self.conf)

    @mock.patch('keystoneauth1.session.Session.get_token',
                return_value='fake-token')
    def test_no_token(self, fake_session):
        test_endpoint = 'http://example.org:8888'
        keystone_session = session.Session()

        with mock.patch.object(self.auth, '_get_endpoint') as get_endpoint:
            with mock.patch.object(self.auth,
                                   '_get_keystone_session') as get_session:

                get_endpoint.return_value = test_endpoint
                get_session.return_value = keystone_session

                req = self.auth.authenticate(1, request.Request())
                self.assertEqual(test_endpoint, req.endpoint)
                self.assertIn('X-Auth-Token', req.headers)
                self.assertIn(req.headers['X-Auth-Token'], 'fake-token')

    def test_with_token(self):
        self.auth.conf.update({"auth_token": "test-token"})
        req = request.Request(endpoint='http://example.org:8888')
        req = self.auth.authenticate(1, req)
        self.assertIn('X-Auth-Token', req.headers)
        self.assertIn(req.headers['X-Auth-Token'], 'test-token')
