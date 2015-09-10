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

import json
import mock

from zaqarclient.queues.v1 import iterator
from zaqarclient.tests.queues import base
from zaqarclient.transport import errors
from zaqarclient.transport import response


class QueuesV1PoolUnitTest(base.QueuesTestBase):

    def test_pool_create(self):
        pool_data = {'weight': 10,
                     'uri': 'sqlite://'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.side_effect = iter([errors.ResourceNotFound, resp])

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            pool = self.client.pool('test', **pool_data)
            self.assertEqual(pool.name, 'test')
            self.assertEqual(pool.weight, 10)

    def test_pool_get(self):
        pool_data = {'weight': 10,
                     'uri': 'sqlite://',
                     'options': {}}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(pool_data))
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            pool = self.client.pool('test')
            self.assertEqual(pool.name, 'test')
            self.assertEqual(pool.weight, 10)

    def test_pool_update(self):
        pool_data = {'weight': 10,
                     'uri': 'sqlite://',
                     'options': {}}
        updated_data = {'weight': 20,
                        'uri': 'sqlite://',
                        'options': {}}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(updated_data))
            send_method.return_value = resp

            pool = self.client.pool('test', **pool_data)
            pool.update({'weight': 20})
            self.assertEqual(20, pool.weight)

    def test_pool_list(self):
        returned = {
            'links': [{
                'rel': 'next',
                'href': '/v1.1/pools?marker=6244-244224-783'
            }],
            'pools': [{
                'name': 'stomach',
                'weight': 20,
                'uri': 'sqlite://',
                'options': {}
            }]
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            pools_var = self.client.pools(limit=1)
            self.assertIsInstance(pools_var, iterator._Iterator)
            self.assertEqual(1, len(list(pools_var)))

    def test_pool_delete(self):
        pool_data = {'weight': 10,
                     'uri': 'sqlite://',
                     'options': {}}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            resp_data = response.Response(None, json.dumps(pool_data))
            send_method.side_effect = iter([resp_data, resp])
            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            pool = self.client.pool('test', **pool_data)
            pool.delete()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1_1PoolFunctionalTest(base.QueuesTestBase):

    def test_pool_get(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}

        self.client.pool('test', **pool_data)
        pool = self.client.pool('test')

        self.assertEqual(pool.name, 'test')
        self.assertEqual(pool.weight, 10)
        self.assertEqual(pool.uri, 'mongodb://127.0.0.1:27017')

    def test_pool_create(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}

        pool = self.client.pool('test', **pool_data)
        self.addCleanup(pool.delete)
        self.assertEqual(pool.name, 'test')
        self.assertEqual(pool.weight, 10)

    def test_pool_update(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}

        pool = self.client.pool('test', **pool_data)
        self.addCleanup(pool.delete)
        pool.update({'weight': 20})
        self.assertEqual(20, pool.weight)

    def test_pool_list(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}
        pool = self.client.pool('test', **pool_data)
        self.addCleanup(pool.delete)

        pools = self.client.pools()
        self.assertTrue(isinstance(pools, iterator._Iterator))
        self.assertEqual(1, len(list(pools)))

    def test_pool_delete(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}

        pool = self.client.pool('test', **pool_data)
        pool.delete()
