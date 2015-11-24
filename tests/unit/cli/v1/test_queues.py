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

from tests.unit.cli import fakes

from zaqarclient.queues.v1 import cli as v1_cli
from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v1 import queues as v1_api_queues


class TestQueues(fakes.TestMessaging):
    def setUp(self):
        super(TestQueues, self).setUp()


class TestV1ListQueues(TestQueues):
    def setUp(self):
        super(TestV1ListQueues, self).setUp()
        queues_list = iterator._Iterator(self, [{'name': 'fake_queue'}],
                                         'queues',
                                         v1_api_queues.create_object(self))
        self.app.client_manager.messaging.queues.return_value = queues_list

        # Command to test
        self.cmd = v1_cli.ListQueues(self.app, None)

    def test_queues_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        expected_columns = ('Name',)
        self.assertEqual(expected_columns, columns)
        # Check that data is correct
        expected_data = [('fake_queue',)]
        self.assertEqual(expected_data, list(data))


class TestV1CreateQueue(TestQueues):

    def setUp(self):
        super(TestV1CreateQueue, self).setUp()

        # Command to test
        self.cmd = v1_cli.CreateQueue(self.app, None)

    def test_queue_create(self):
        arglist = ['fake_queue']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.messaging_client.queue.assert_called_with('fake_queue',
                                                       force_create=True)
