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

from zaqarclient.tests import base
from zaqarclient.transport import request


HREF = '/v1/queue/'


class TestRequest(base.TestBase):

    def test_prepare_request(self):
        req = request.prepare_request(self.conf)
        self.assertTrue(isinstance(req, request.Request))
        self.assertIsNone(req.content)

    def test_prepare_request_with_data(self):
        data = {"data": "tons of GBs"}
        req = request.prepare_request(self.conf, data=data)
        self.assertTrue(isinstance(req, request.Request))
        self.assertEqual(req.content, json.dumps(data))
