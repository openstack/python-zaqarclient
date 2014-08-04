# Copyright (c) 2014 Red Hat, Inc.
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

from zaqarclient.tests.queues import base
from zaqarclient.transport import response


class QueuesV1ShardUnitTest(base.QueuesTestBase):

    def test_shard_create(self):
        shard_data = {'weight': 10,
                      'uri': 'sqlite://'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            shard = self.client.shard('test', **shard_data)
            self.assertEqual(shard.name, 'test')
            self.assertEqual(shard.weight, 10)

    def test_shard_delete(self):
        shard_data = {'weight': 10,
                      'uri': 'sqlite://'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            shard = self.client.shard('test', **shard_data)
            shard.delete()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1ShardFunctionalTest(base.QueuesTestBase):

    def test_shard_create(self):
        shard_data = {'weight': 10,
                      'uri': 'sqlite://'}

        shard = self.client.shard('test', **shard_data)
        self.assertEqual(shard.name, 'test')
        self.assertEqual(shard.weight, 10)

    def test_shard_delete(self):
        shard_data = {'weight': 10,
                      'uri': 'sqlite://'}

        shard = self.client.shard('test', **shard_data)
        shard.delete()
