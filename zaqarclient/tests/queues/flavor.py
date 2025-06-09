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
from unittest import mock

from zaqarclient.queues.v2 import iterator
from zaqarclient.tests.queues import base
from zaqarclient.transport import response


class QueuesV2FlavorUnitTest(base.QueuesTestBase):

    def test_flavor_create(self):
        pool_list = ['pool1', 'pool2']
        flavor_data = {'pool_list': pool_list}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            flavor = self.client.flavor('tasty', **flavor_data)
            self.assertEqual('tasty', flavor.name)

    def test_flavor_get(self):
        flavor_data = {'name': 'test'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(flavor_data))
            send_method.return_value = resp

            # NOTE(flaper87): This will call
            # ensure exists in the client instance
            # since auto_create's default is True
            flavor = self.client.flavor('test')
            flavor1 = flavor.get()
            self.assertEqual('test', flavor1['name'])

    def test_flavor_update(self):
        pool_list1 = ['pool1', 'pool2']
        pool_list2 = ['pool3', 'pool4']
        flavor_data = {'pool_list': pool_list1}
        updated_data = {'pool_list': pool_list2}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, json.dumps(updated_data))
            send_method.return_value = resp

            flavor = self.client.flavor('tasty', **flavor_data)
            flavor.update({'pool_list': pool_list2})
            self.assertEqual(pool_list2, flavor.pool_list)

    def test_flavor_list(self):
        returned = {
            'links': [{
                'rel': 'next',
                'href': '/v2/flavors?marker=6244-244224-783'
            }],
            'flavors': [{
                'name': 'tasty'
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
        pool_list = ['pool1', 'pool2']
        flavor_data = {'pool_list': pool_list}

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


class QueuesV2FlavorFunctionalTest(base.QueuesTestBase):

    def test_flavor_create(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'flavor': 'tasty'}
        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)
        pool_list = ['stomach']
        flavor_data = {'pool_list': pool_list}
        flavor = self.client.flavor('tasty', **flavor_data)
        self.addCleanup(flavor.delete)

        self.assertEqual('tasty', flavor.name)
        self.assertEqual(pool_list, flavor.pool_list)

    def test_flavor_get(self):
        pool_data = {'weight': 10,
                     'flavor': 'tasty',
                     'uri': 'mongodb://127.0.0.1:27017'}
        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        pool_list = ['stomach']
        flavor_data = {'pool_list': pool_list}
        flavor = self.client.flavor('tasty', **flavor_data)
        resp_data = flavor.get()
        self.addCleanup(flavor.delete)

        self.assertEqual('tasty', resp_data['name'])

    def test_flavor_update(self):
        pool_data = {'weight': 10,
                     'uri': 'mongodb://127.0.0.1:27017',
                     'flavor': 'tasty'}

        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        pool_list = ['stomach']
        flavor_data = {'pool_list': pool_list}
        flavor = self.client.flavor('tasty', **flavor_data)
        self.addCleanup(flavor.delete)

    def test_flavor_list(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'flavor': 'test_flavor'}

        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        pool_list = ['stomach']
        flavor_data = {'pool_list': pool_list}
        flavor = self.client.flavor("test_flavor", **flavor_data)
        self.addCleanup(flavor.delete)

        flavors = self.client.flavors()
        self.assertIsInstance(flavors, iterator._Iterator)
        self.assertEqual(1, len(list(flavors)))

    def test_flavor_delete(self):
        pool_data = {'uri': 'mongodb://127.0.0.1:27017',
                     'weight': 10,
                     'flavor': 'tasty'}
        pool = self.client.pool('stomach', **pool_data)
        self.addCleanup(pool.delete)

        pool_list = ['stomach']
        flavor_data = {'pool_list': pool_list}
        flavor = self.client.flavor('tasty', **flavor_data)
        flavor.delete()
