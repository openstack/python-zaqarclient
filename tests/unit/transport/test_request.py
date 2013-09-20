# Copyright (c) 2013 Rackspace, Inc.
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

from marconiclient.tests import base
from marconiclient.transport import request


HREF = '/v1/queue/'


class TestRequest(base.TestBase):
    def test_valid_operation(self):
        req = request.Request(endpoint=HREF, operation='create_queue',
                              params=dict(queue_name='high_load'))
        self.assertIs(None, req.validate())

    def test_invalid_operation(self):
        req = request.Request(endpoint=HREF, operation='jump_queue',
                              params=dict(name='high_load'))
        self.assertEqual("Invalid operation 'jump_queue'", req.validate())

    def test_missing_mandatory_param(self):
        req = request.Request(endpoint=HREF, operation='get_message',
                              params=dict())
        self.assertEqual("Missing mandatory params: 'message_id, queue_name'",
                         req.validate())

    def test_missing_optional_param(self):
        req = request.Request(endpoint=HREF, operation='delete_message',
                              params=dict(queue_name='abc', message_id='1'))
        self.assertIs(None, req.validate())

    def test_invalid__param(self):
        req = request.Request(endpoint=HREF, operation='delete_queue',
                              params=dict(queue_name='xy', WAT='!?'))
        self.assertEqual("Invalid params: 'WAT'", req.validate())
