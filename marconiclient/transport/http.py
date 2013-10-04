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

from marconiclient.common import http
from marconiclient.transport import base


class HttpTransport(base.Transport):

    def __init__(self, conf):
        super(HttpTransport, self).__init__(conf)
        self.client = http.Client()

    def _prepare(self, request):
        if not request.api:
            return request.endpoint, 'GET', request

        # TODO(flaper87): Validate if the user
        # explicitly wants so. Validation must
        # happen before any other operation here.
        # request.validate()

        schema = request.api.get_schema(request.operation)
        ref = schema.get('ref', '')
        ref_params = {}

        for param in list(request.params.keys()):
            if '{{{0}}}'.format(param) in ref:
                ref_params[param] = request.params.pop(param)

        url = '{0}/{1}'.format(request.endpoint.rstrip('/'),
                               ref.format(**ref_params))
        return url, schema.get('method', 'GET'), request

    def send(self, request):
        url, method, request = self._prepare(request)

        # NOTE(flape87): Do not modify
        # request's headers directly.
        headers = request.headers.copy()
        headers['content-type'] = 'application/json'

        return self.client.request(method,
                                   url=url,
                                   params=request.params,
                                   headers=headers,
                                   data=request.content)
