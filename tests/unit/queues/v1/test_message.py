# Copyright (c) 2013 Rackspace, Inc.
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

from zaqarclient.queues.v1 import iterator as iterate
from zaqarclient.queues.v1 import message
from zaqarclient.tests.queues import base
from zaqarclient.tests.queues import messages as test_message
from zaqarclient.transport import http
from zaqarclient.transport import response


class TestMessageIterator(base.QueuesTestBase):

    def test_no_next_iteration(self):
        messages = {'links': [],
                    'messages': [{
                        'href': '/v1/queues/mine/messages/123123423',
                        'ttl': 800,
                        'age': 790,
                        'body': {'event': 'ActivateAccount',
                                 'mode': 'active'}
                    }]
                    }

        iterator = iterate._Iterator(self.queue.client,
                                     messages,
                                     'messages',
                                     message.create_object(self.queue))
        iterated = [msg for msg in iterator]
        self.assertEqual(1, len(iterated))

    def test_stream(self):
        messages = {'links': [],
                    'messages': [{
                        'href': '/v1/queues/mine/messages/123123423',
                        'ttl': 800,
                        'age': 790,
                        'body': {'event': 'ActivateAccount',
                                 'mode': 'active'}
                    }]
                    }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(messages))
            send_method.return_value = resp

            # NOTE(flaper87): The first iteration will return 1 message
            # and then call `_next_page` which will use the rel-next link
            # to get a new set of messages.
            link = {'rel': 'next',
                    'href': "/v1/queues/mine/messages?marker=6244-244224-783"}
            messages['links'].append(link)

            iterator = iterate._Iterator(self.queue.client,
                                         messages,
                                         'messages',
                                         message.create_object(self.queue))
            iterated = [msg for msg in iterator.stream()]
            self.assertEqual(2, len(iterated))

    def test_iterator_respect_paging(self):
        messages = {'links': [],
                    'messages': [{
                        'href': '/v1/queues/mine/messages/123123423',
                        'ttl': 800,
                        'age': 790,
                        'body': {'event': 'ActivateAccount',
                                 'mode': 'active'}
                    }]
                    }

        with mock.patch.object(self.transport, 'send',
                               autospec=True) as send_method:

            resp = response.Response(None, json.dumps(messages))
            send_method.return_value = resp

            link = {'rel': 'next',
                    'href': "/v1/queues/mine/messages?marker=6244-244224-783"}
            messages['links'].append(link)

            iterator = iterate._Iterator(self.queue.client,
                                         messages,
                                         'messages',
                                         message.create_object(self.queue))
            iterated = [msg for msg in iterator]
            self.assertEqual(1, len(iterated))


class QueuesV1MessageHttpUnitTest(test_message.QueuesV1MessageUnitTest):

    transport_cls = http.HttpTransport
    url = 'http://127.0.0.1:8888/v1'
    version = 1


class QueuesV1_1MessageHttpUnitTest(test_message.QueuesV1MessageUnitTest):

    transport_cls = http.HttpTransport
    url = 'http://127.0.0.1:8888/v1.1'
    version = 1.1
