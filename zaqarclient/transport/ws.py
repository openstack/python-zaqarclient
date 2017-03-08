#   Copyright 2016 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import json
import uuid

from oslo_log import log as logging
from oslo_utils import importutils

from zaqarclient.transport import base
from zaqarclient.transport import request
from zaqarclient.transport import response

websocket = importutils.try_import('websocket')

LOG = logging.getLogger(__name__)


class WebsocketTransport(base.Transport):

    """Zaqar websocket transport.

    *NOTE:* Zaqar's websocket interface does not yet appear to work
    well with parameters. Until it does the websocket transport may not
    integrate with all of zaqarclients higherlevel request. Even so...
    websockets today is still quite usable and use of the transport
    via lower level API's in zaqarclient work quite nicely. Example:

       conf = {
            'auth_opts': {
                'backend': 'keystone',
                'options': {
                    'os_auth_token': ks.auth_token,
                    'os_project_id': CONF.zaqar.project_id
                }
            }
        }

        endpoint = 'ws://172.19.0.3:9000'

        with transport.get_transport_for(endpoint, options=conf) as ws:
            req = request.Request(endpoint, 'queue_create',
                                  content=json.dumps({'queue_name': 'foo'}))
            resp = ws.send(req)

    """
    def __init__(self, options):
        super(WebsocketTransport, self).__init__(options)
        option = options['auth_opts']['options']
        # TODO(wangxiyuan): To keep backwards compatibility, we leave
        # "os_project_id" here. Remove it in the next release.
        self._project_id = option.get('os_project_id',
                                      option.get('project_id'))
        self._token = options['auth_opts']['options']['os_auth_token']
        self._websocket_client_id = None
        self._ws = None

    def _init_client(self, endpoint):
        """Initialize a websocket transport client.

        :param endpoint: The websocket endpoint. Example: ws://127.0.0.1:9000/.
                         Required.
        :type endpoint: string
        """
        self._websocket_client_id = str(uuid.uuid4())

        LOG.debug('Instantiating messaging websocket client: %s', endpoint)
        self._ws = self._create_connection(endpoint)

        auth_req = request.Request(endpoint, 'authenticate',
                                   headers={'X-Auth-Token': self._token})
        self.send(auth_req)

    def _create_connection(self, endpoint):
        return websocket.create_connection(endpoint)

    def send(self, request):
        if not self._ws:
            self._init_client(request.endpoint)

        headers = request.headers.copy()
        headers.update({
            'Client-ID': self._websocket_client_id,
            'X-Project-ID': self._project_id
        })

        msg = {'action': request.operation, 'headers': headers}
        if request.content:
            msg['body'] = json.loads(request.content)
        # NOTE(dprince): Zaqar websockets do not yet seem to support params?!
        # Users of this protocol will need to send everything in the body.
        if request.params:
            LOG.warning('Websocket transport does not yet support params.')
        self._ws.send(json.dumps(msg))
        ret = self.recv()

        resp = response.Response(request, json.dumps(ret.get('body', '')),
                                 headers=ret['headers'],
                                 status_code=int(ret['headers']['status']))

        if resp.status_code in self.http_to_zaqar:
            kwargs = {}
            try:
                error_body = json.loads(resp.content)
                kwargs['title'] = 'Websocket Transport Error'
                kwargs['description'] = error_body['error']
            except Exception:
                kwargs['text'] = resp.content
            raise self.http_to_zaqar[resp.status_code](**kwargs)

        return resp

    def recv(self):
        return json.loads(self._ws.recv())

    def cleanup(self):
        if self._ws:
            self._ws.close()
            self._ws = None

    def __enter__(self):
        """Return self to allow usage as a context manager"""
        return self

    def __exit__(self, *exc):
        """Call cleanup when exiting the context manager"""
        self.cleanup()
