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
from unittest import mock

from zaqarclient.queues.v2 import core
from zaqarclient.tests import base
from zaqarclient.tests.transport import dummy
from zaqarclient.transport import errors
from zaqarclient.transport import request
from zaqarclient.transport import response


class TestV2Core(base.TestBase):

    def setUp(self):
        super(TestV2Core, self).setUp()
        self.transport = dummy.DummyTransport(self.conf)

    def test_queue_create(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.return_value = response.Response(None, None)

            req = request.Request()
            core.queue_create(self.transport, req, 'test')
            self.assertIn('queue_name', req.params)

    def test_queue_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.return_value = response.Response(None, None)

            req = request.Request()
            core.queue_delete(self.transport, req, 'test')
            self.assertIn('queue_name', req.params)

    def test_queue_exists(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.return_value = response.Response(None, None)

            req = request.Request()
            ret = core.queue_exists(self.transport, req, 'test')
            self.assertIn('queue_name', req.params)
            self.assertTrue(ret)

    def test_queue_exists_not_found(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            send_method.side_effect = errors.ResourceNotFound

            req = request.Request()
            ret = core.queue_exists(self.transport, req, 'test')
            self.assertIn('queue_name', req.params)
            self.assertFalse(ret)

    def test_get_queue_metadata(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()
            core.queue_get_metadata(self.transport, req, 'test')

    def test_set_queue_metadata(self):
        update_data = {'some': 'data'}
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            send_method.return_value = response.Response(None, None)

            req = request.Request()
            core.queue_exists(self.transport, req, update_data, 'test')
            self.assertIn('queue_name', req.params)

    def test_queue_get_stats(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()
            result = core.queue_get_stats(self.transport, req, 'test')
            self.assertEqual({}, result)

    def test_message_post_one(self):
        messages = {'ttl': 30, 'body': 'Post one!'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()

            core.message_post(self.transport, req, 'test', messages)
            self.assertIn('queue_name', req.params)
            self.assertEqual(messages, json.loads(req.content))

    def test_message_post_many(self):
        messages = [{'ttl': 30, 'body': 'Post one!'},
                    {'ttl': 30, 'body': 'Post two!'},
                    {'ttl': 30, 'body': 'Post three!'}, ]

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()

            core.message_post(self.transport, req, 'test', messages)
            self.assertIn('queue_name', req.params)
            self.assertEqual(messages, json.loads(req.content))

    def test_message_list(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()

            core.message_list(self.transport, req, 'test')
            self.assertIn('queue_name', req.params)

    def test_message_list_kwargs(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()

            core.message_list(self.transport, req, 'test',
                              marker='supermarket',
                              echo=False, limit=10)

            self.assertIn('queue_name', req.params)
            self.assertIn('limit', req.params)
            self.assertIn('echo', req.params)
            self.assertIn('marker', req.params)

    def test_message_get_many(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()

            ids = ['a', 'b']
            core.message_get_many(self.transport, req,
                                  'test', ids)

            self.assertIn('queue_name', req.params)
            self.assertIn('ids', req.params)
            self.assertEqual(ids, req.params['ids'])

    def test_message_get(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, '{}')
            send_method.return_value = resp

            req = request.Request()
            core.message_get(self.transport, req,
                             'test', 'message_id')

    def test_message_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            req = request.Request()
            core.message_delete(self.transport, req,
                                'test', 'message_id')

    def test_message_delete_many(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            ids = ['a', 'b']
            req = request.Request()
            core.message_delete_many(self.transport, req,
                                     'test', ids=ids)

            self.assertIn('queue_name', req.params)
            self.assertIn('ids', req.params)
            self.assertEqual(ids, req.params['ids'])

    # ADMIN API
    def test_pool_create(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            req = request.Request()
            core.pool_create(self.transport, req,
                             'test_pool', {'uri': 'sqlite://',
                                           'weight': 0})

    def test_pool_get(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            req = request.Request()
            core.pool_get(self.transport, req,
                          'test_pool')

    def test_pool_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            req = request.Request()
            core.pool_delete(self.transport, req, 'test_pool')

    def test_health(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:
            resp = response.Response(None, None)
            send_method.return_value = resp

            req = request.Request()
            core.health(self.transport, req)
