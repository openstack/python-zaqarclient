# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import mock

from zaqarclient.tests import base
from zaqarclient.transport import request
from zaqarclient.transport import ws


class TestWsTransport(base.TestBase):

    def setUp(self):
        super(TestWsTransport, self).setUp()
        os_opts = {
            'os_auth_token': 'FAKE_TOKEN',
            'os_auth_url': 'http://127.0.0.0:5000/v3',
            'os_project_id': 'admin',
            'os_service_type': 'messaging-websocket',
        }
        auth_opts = {'backend': 'keystone',
                     'options': os_opts}
        self.options = {'auth_opts': auth_opts}
        self.endpoint = 'ws://127.0.0.1:9000'

    @mock.patch.object(ws.WebsocketTransport, "_create_connection")
    def test_make_client(self, ws_create_connection):
        ws_create_connection.return_value.recv.return_value = json.dumps({
            "headers": {
                "status": 200
            }
        })

        transport = ws.WebsocketTransport(self.options)
        req = request.Request(self.endpoint)
        transport.send(req)
        ws_create_connection.assert_called_with("ws://127.0.0.1:9000")

    @mock.patch.object(ws.WebsocketTransport, "recv")
    @mock.patch.object(ws.WebsocketTransport, "_create_connection")
    def test_recv(self, ws_create_connection, recv_mock):

        send_ack = {
            "headers": {
                "status": 200
            }
        }

        recv_mock.side_effect = [send_ack, send_ack, send_ack, {
            "body": {
                "payload": "foo"
            }
        }, send_ack]

        transport = ws.WebsocketTransport(self.options)
        req = request.Request(self.endpoint)
        transport.send(req)

        count = 0

        while True:
            count += 1
            data = transport.recv()
            if 'body' in data:
                self.assertEqual(data['body']['payload'], 'foo')
                break
            if count >= 4:
                self.fail('Failed to receive expected message.')
