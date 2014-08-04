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

from zaqarclient.common import http
from zaqarclient.tests import base


class TestCommonHttp(base.TestBase):

    def setUp(self):
        super(TestCommonHttp, self).setUp()
        self.client = http.Client()

    def test_data_serialization(self):
        data = {'some': 'data'}

        for method in ['post', 'put', 'patch']:
            with mock.patch.object(self.client.session, method,
                                   autospec=True) as request_method:
                request_method.return_value = True
                getattr(self.client, method)("url", data=data)
                request_method.assert_called_with('url', data=json.dumps(data))
