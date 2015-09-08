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


class QueuesV1_1FlavorUnitTest(base.QueuesTestBase):

    url = 'http://127.0.0.1:8888/v1.1'
    version = 1.1

    def test_flavor_create(self):
        flavor_data = {'pool': 'stomach'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.side_effect = iter([errors.ResourceNotFound, resp])

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            flavor = self.client.flavor('tasty', **flavor_data)
            self.assertEqual(flavor.name, 'tasty')
            self.assertEqual(flavor.pool, 'stomach')

    def test_flavor_get(self):
        flavor_data = {'pool': 'stomach'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(flavor_data))
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            flavor = self.client.flavor('test')
            self.assertEqual(flavor.name, 'test')
            self.assertEqual(flavor.pool, 'stomach')

    def test_flavor_update(self):
        flavor_data = {'pool': 'stomach'}
        updated_data = {'pool': 'belly'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, json.dumps(updated_data))
            send_method.return_value = resp

            flavor = self.client.flavor('tasty', **flavor_data)
            flavor.update({'pool': 'belly'})
            self.assertEqual('belly', flavor.pool)

    def test_flavor_list(self):
        returned = {
            'links': [{
                'rel': 'next',
                'href': '/v1.1/flavors?marker=6244-244224-783'
            }],
            'flavors': [{
                'name': 'tasty',
                'pool': 'stomach'
            }]
        }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(returned))
            send_method.return_value = resp

            flavor_var = self.client.flavors(limit=1)
            self.assertIsInstance(flavor_var, iterator._Iterator)
            self.assertEqual(1, len(list(flavor_var)))

    def test_flavor_delete(self):
        flavor_data = {'pool': 'stomach'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            resp_data = response.Response(None, json.dumps(flavor_data))
            send_method.side_effect = iter([resp_data, resp])
            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            flavor = self.client.flavor('tasty', **flavor_data)
            flavor.delete()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1_1FlavorFunctionalTest(base.QueuesTestBase):

    url = 'http://127.0.0.1:8888/v1.1'
    version = 1.1

    def test_flavor_create(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'group': 'us'}
        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        flavor_data = {'pool': 'us'}
        flavor = self.client.flavor('tasty', **flavor_data)
        self.addCleanup(flavor.delete)

        self.assertEqual(flavor.name, 'tasty')
        self.assertEqual(flavor.pool, 'us')

    def test_flavor_get(self):
        pool_data = {'weight': 10,
                     'group': 'us',
                     'uri': 'mongodb://127.0.0.1:27017'}
        self.client.pool('stomach', **pool_data)

        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        flavor_data = {'pool': 'us'}
        self.client.flavor('tasty', **flavor_data)
        flavor = self.client.flavor('tasty')
        self.addCleanup(flavor.delete)

        self.assertEqual(flavor.name, 'tasty')
        self.assertEqual(flavor.pool, 'us')

    def test_flavor_update(self):
        pool_data = {'weight': 10,
                     'uri': 'mongodb://127.0.0.1:27017',
                     'group': 'us'}

        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        flavor_data = {'pool': 'us'}
        flavor = self.client.flavor('tasty', **flavor_data)
        self.addCleanup(flavor.delete)
        pool.update({'group': 'belly'})
        flavor.update({'pool': 'belly'})
        self.assertEqual('belly', flavor.pool)

    def test_flavor_list(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'group': 'us'}

        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        flavor_data = {'pool': 'us'}
        flavor = self.client.flavor("test_flavor", **flavor_data)
        self.addCleanup(flavor.delete)

        flavors = self.client.flavors()
        self.assertTrue(isinstance(flavors, iterator._Iterator))
        self.assertEqual(1, len(list(flavors)))

    def test_flavor_delete(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'group': 'us'}
        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        flavor_data = {'pool': 'us'}
        flavor = self.client.flavor('tasty', **flavor_data)
        flavor.delete()
