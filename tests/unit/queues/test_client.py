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

from marconiclient import errors
from marconiclient.queues import client
from marconiclient.tests import base


class TestClient(base.TestBase):

    def test_get_instance(self):
        version = list(client._CLIENTS.keys())[0]
        cli = client.Client('http://example.com',
                            version, {})
        self.assertTrue(isinstance(cli,
                                   client._CLIENTS[version]))

    def test_version_failure(self):
        self.assertRaises(errors.MarconiError,
                          client.Client,
                          'http://example.org',
                          -1, {})
