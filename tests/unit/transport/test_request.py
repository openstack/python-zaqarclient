# Copyright (c) 2013 Rackspace, Inc.
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

from zaqarclient.queues.v1 import api as api_v1
from zaqarclient.queues.v2 import api as api_v2
from zaqarclient.tests import base
from zaqarclient.transport import request


class TestRequest(base.TestBase):

    def test_request_project_id(self):
        auth_opts = {
            'options': {
                'os_project_id': 'my-project'
            }
        }
        auth_opts.update({'backend': 'noauth'})
        req = request.prepare_request(auth_opts)
        self.assertEqual('my-project', req.headers['X-Project-Id'])

    def test_prepare_request(self):
        auth_opts = self.conf.get('auth_opts', {})
        req = request.prepare_request(auth_opts)
        self.assertIsInstance(req, request.Request)
        self.assertIsNone(req.content)

    def test_prepare_request_with_data(self):
        auth_opts = self.conf.get('auth_opts', {})
        data = {"data": "tons of GBs"}
        req = request.prepare_request(auth_opts, data=data)
        self.assertIsInstance(req, request.Request)
        self.assertEqual(json.dumps(data), req.content)

    def test_request_with_right_version(self):
        auth_opts = self.conf.get('auth_opts', {})
        api_version = 1
        req = request.prepare_request(auth_opts, api=api_version)
        self.assertIsInstance(req.api, api_v1.V1)

        api_version = 1.0
        req = request.prepare_request(auth_opts, api=api_version)
        self.assertIsInstance(req.api, api_v1.V1)

        api_version = 1.1
        req = request.prepare_request(auth_opts, api=api_version)
        self.assertIsInstance(req.api, api_v1.V1_1)

        api_version = 2
        req = request.prepare_request(auth_opts, api=api_version)
        self.assertIsInstance(req.api, api_v2.V2)

        api_version = 2.0
        req = request.prepare_request(auth_opts, api=api_version)
        self.assertIsInstance(req.api, api_v2.V2)
