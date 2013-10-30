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

import os

import json
import mock
import testtools

from marconiclient.queues.v1 import client
from marconiclient.tests import base
from marconiclient.transport import response

_RUN_FUNCTIONAL = os.environ.get('MARCONICLIENT_TEST_FUNCTIONAL', False)


class QueuesV1QueueTestBase(base.TestBase):

    transport_cls = None

    # NOTE(flaper87): These class attributes
    # are intended for functional tests only
    # and will be replaced with something
    # dynamically loaded to allow tests against
    # remote instances.
    url = None
    version = None

    def setUp(self):
        super(QueuesV1QueueTestBase, self).setUp()
        self.transport = self.transport_cls(self.conf)

        self.client = client.Client(self.conf, self.url,
                                    self.version)

        # NOTE(flaper87): Nasty monkeypatch, lets use
        # the dummy transport here.
        #setattr(self.client, 'transport', self.transport)
        self.queue = self.client.queue(1, auto_create=False)
        self.queue._get_transport = mock.Mock(return_value=self.transport)

        self.is_functional = _RUN_FUNCTIONAL

    def test_queue_metadata(self):
        test_metadata = {'type': 'Bank Accounts'}

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(test_metadata))
            send_method.return_value = resp

            metadata = self.queue.metadata()
            self.assertEqual(metadata, test_metadata)

    def test_queue_create(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.ensure_exists()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_delete(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.delete()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.

    def test_queue_exists(self):
        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, None)
            send_method.return_value = resp

            self.queue.exists()

            # NOTE(flaper87): Nothing to assert here,
            # just checking our way down to the transport
            # doesn't crash.


class QueuesV1QueueFuncMixin(object):

    @testtools.skipUnless(_RUN_FUNCTIONAL,
                          'Functional tests disabled')
    def test_queue_create_functional(self):
        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertTrue(queue.exists())

    @testtools.skipUnless(_RUN_FUNCTIONAL,
                          'Functional tests disabled')
    def test_queue_delete_functional(self):
        queue = self.client.queue("nonono")
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertTrue(queue.exists())
        queue.delete()
        self.assertFalse(queue.exists())

    @testtools.skipUnless(_RUN_FUNCTIONAL,
                          'Functional tests disabled')
    def test_queue_exists_functional(self):
        queue = self.client.queue("404", auto_create=False)
        queue._get_transport = mock.Mock(return_value=self.transport)
        self.assertFalse(queue.exists())

    @testtools.skipUnless(_RUN_FUNCTIONAL,
                          'Functional tests disabled')
    def test_queue_metadata_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Clear metadata's cache
        queue._metadata = None
        metadata = queue.metadata()
        self.assertEqual(metadata, test_metadata)

    @testtools.skipUnless(_RUN_FUNCTIONAL,
                          'Functional tests disabled')
    def test_queue_metadata_reload_functional(self):
        test_metadata = {'type': 'Bank Accounts'}
        queue = self.client.queue("meta-test")
        queue.metadata(test_metadata)

        # NOTE(flaper87): Overwrite the cached value
        # but don't clear it.
        queue._metadata = 'test'
        metadata = queue.metadata(force_reload=True)
        self.assertEqual(metadata, test_metadata)
