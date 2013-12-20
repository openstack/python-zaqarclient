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

import uuid

from marconiclient.queues.v1 import queues
from marconiclient import transport
from marconiclient.transport import request


class Client(object):
    """Client base class

    :param url: Marconi's instance base url.
    :type url: `six.text_type`
    :param version: API Version pointing to.
    :type version: `int`
    :param options: Extra options:
        - client_uuid: Custom client uuid. A new one
        will be generated, if not passed.
        - auth_opts: Authentication options:
            - backend
            - options
    :type options: `dict`
    """

    def __init__(self, url=None, version=1, conf=None):
        self.conf = conf or {}

        self.api_url = url
        self.api_version = version
        self.auth_opts = self.conf.get('auth_opts', {})
        self.client_uuid = self.conf.get('client_uuid',
                                         uuid.uuid4().hex)

    def _get_transport(self, request):
        """Gets a transport and caches its instance

        This method gets a transport instance based on
        the request's endpoint and caches that for later
        use. The transport instance is invalidated whenever
        a session expires.

        :param request: The request to use to load the
            transport instance.
        :type request: `transport.request.Request`
        """

        trans = transport.get_transport_for(request,
                                            options=self.conf)
        return (trans or self.transport)

    def _request_and_transport(self):
        api = 'queues.v' + str(self.api_version)
        req = request.prepare_request(self.auth_opts,
                                      endpoint=self.api_url,
                                      api=api)

        req.headers['Client-ID'] = self.client_uuid

        trans = self._get_transport(req)
        return req, trans

    def transport(self):
        """Gets a transport based the api url and version."""
        return transport.get_transport_for(self.url,
                                           self.api_version)

    def queue(self, ref, **kwargs):
        """Returns a queue instance

        :param ref: Queue's reference id.
        :type ref: `six.text_type`

        :returns: A queue instance
        :rtype: `queues.Queue`
        """
        return queues.Queue(self, ref, **kwargs)

    def follow(self, ref):
        """Follows ref.

        :params ref: The reference path.
        :type ref: `six.text_type`
        """
        req, trans = self._request_and_transport()
        req.ref = ref

        return trans.send(req).deserialized_content
