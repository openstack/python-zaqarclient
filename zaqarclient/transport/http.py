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

from zaqarclient.common import http
from zaqarclient.transport import base
# NOTE(flaper87): Something is completely borked
# with some imports. Using `from ... import errors`
# will end up importing `zaqarclient.errors` instead
# of transports
import zaqarclient.transport.errors as errors
from zaqarclient.transport import response


class HttpTransport(base.Transport):

    http_to_zaqar = {
        400: errors.MalformedRequest,
        401: errors.UnauthorizedError,
        403: errors.ForbiddenError,
        404: errors.ResourceNotFound,
        500: errors.InternalServerError,
        503: errors.ServiceUnavailableError
    }

    def __init__(self, options):
        super(HttpTransport, self).__init__(options)
        self.client = http.Client()

    def _prepare(self, request):
        if not request.api:
            return request.endpoint, 'GET', request

        # TODO(flaper87): Validate if the user
        # explicitly wants so. Validation must
        # happen before any other operation here.
        # request.validate()

        schema = {}
        ref_params = {}
        ref = request.ref

        if request.operation:
            schema = request.api.get_schema(request.operation)
            ref = ref or schema.get('ref', '')

        # FIXME(flaper87): We expect the endpoint
        # to have the API version label already,
        # however in a follow-your-nose implementation
        # it should be the other way around.
        ref = ref.lstrip('/' + request.api.label)

        for param in list(request.params.keys()):
            if '{{{0}}}'.format(param) in ref:
                value = request.params.pop(param)

                # NOTE(flaper87): Zaqar API parses
                # sequences encoded as '1,2,3,4'. Let's
                # encode lists, tuples and sets before
                # sending them to the server.
                if isinstance(value, (list, tuple, set)):
                    value = ','.join(value)

                ref_params[param] = value

        url = '{0}/{1}/{2}'.format(request.endpoint.rstrip('/'),
                                   request.api.label,
                                   ref.format(**ref_params))
        return url, schema.get('method', 'GET'), request

    def send(self, request):
        url, method, request = self._prepare(request)

        # NOTE(flape87): Do not modify
        # request's headers directly.
        headers = request.headers.copy()
        headers['content-type'] = 'application/json'

        resp = self.client.request(method,
                                   url=url,
                                   params=request.params,
                                   headers=headers,
                                   data=request.content)

        if resp.status_code in self.http_to_zaqar:
            try:
                msg = json.loads(resp.text)['description']
            except Exception:
                # TODO(flaper87): Log this exception
                # but don't stop raising the corresponding
                # exception
                msg = ''
            raise self.http_to_zaqar[resp.status_code](msg)

        # NOTE(flaper87): This reads the whole content
        # and will consume any attempt of streaming.
        return response.Response(request, resp.text,
                                 headers=resp.headers)
