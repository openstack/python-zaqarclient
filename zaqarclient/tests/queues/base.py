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

import subprocess
from unittest import mock

from oslo_utils import netutils

from zaqarclient.queues import client
from zaqarclient.tests import base
from zaqarclient.tests.transport import dummy

cmd = 'cat /etc/zaqar/uwsgi.conf | grep http'
MY_HOST_IP = subprocess.run(cmd, shell=True, capture_output=True, text=True)
if len(MY_HOST_IP.stdout.split("= ")) < 2:
    MY_IP = netutils.get_my_ipv4() + ':8888'
else:
    MY_IP = MY_HOST_IP.stdout.split("= ")[1]


class QueuesTestBase(base.TestBase):

    transport_cls = dummy.DummyTransport
    url = 'http://%s' % MY_IP
    version = 1

    def setUp(self):
        super(QueuesTestBase, self).setUp()
        self.transport = self.transport_cls(self.conf)

        self.client = client.Client(self.url, self.version,
                                    self.conf)

        mocked_transport = mock.Mock(return_value=self.transport)
        self.client._get_transport = mocked_transport
        self.queue = self.client.queue(1, auto_create=False)
