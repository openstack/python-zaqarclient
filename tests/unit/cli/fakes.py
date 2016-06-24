# Copyright (c) 2015 Catalyst IT Ltd.
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
from osc_lib.tests import utils


class TestMessaging(utils.TestCommand):

    def setUp(self):
        super(TestMessaging, self).setUp()

        self.messaging_client = mock.MagicMock()
        # TODO(flwang): It would be nice if we can figure out a better way to
        # get the mocked request and transport.
        req_trans = (mock.MagicMock(), mock.MagicMock())
        self.messaging_client._request_and_transport.return_value = req_trans
        self.app.client_manager.messaging = self.messaging_client
