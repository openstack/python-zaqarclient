# Copyright (c) 2013 Rackspace, Inc.
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

from marconiclient import auth
from marconiclient.common import api


def prepare_request(conf, data=None):
    """Prepares a request

    This method takes care of authentication
    and all other steps in the preparation chain.

    The request returned by this call is ready to
    be sent to the server.

    :param conf: `cfg.ConfigOpts` instance to use.
    :type conf: `cfg.ConfigOpts`
    :param data: Optional data to send along with the
        request. If data is not None, it'll be serialized.
    :type data: Any primitive type that is json-serializable.

    :returns: A `Request` instance ready to be sent.
    :rtype: `Request`
    """

    req = Request()
    auth_backend = auth.get_backend(conf)
    # TODO(flaper87): Do something smarter
    # to get the api_version.
    req = auth_backend.authenticate(1, req)

    if data is not None:
        req.content = json.dumps(data)
    return req


class Request(object):
    """General data for a Marconi request

    The idea is to be declarative i.e. specify *what* is desired. It's up to
    the respective transport to turn this into a layer-specific request.

    *NOTE:* This implementation is not definitive and may change.

    :param endpoint: Server's endpoint
    :type endpoint: str
    :param operation: Operation to issue on the endpoint, i.e:
        - get_queues
        - get_messages
    :type operation: str
    :param content: Request's body. Default: None
    :type content: str
    :param params: Query string params. Default: None
    :type params: dict
    :param headers: Request headers. Default: None
    :type headers: dict
    """

    def __init__(self, endpoint='', operation='',
                 content=None, params=None, headers=None):
        self.endpoint = endpoint
        self.operation = operation
        self.content = content
        self.params = params or {}
        self.headers = headers or {}

    def validate(self):
        """`None` if the request data is valid, an error message otherwise.
        Checks the `operation` and the presence of the `params`.
        """
        api_info_data = api.info()
        if self.operation not in api_info_data:
            return "Invalid operation '%s'" % self.operation

        api_info = api_info_data[self.operation]

        param_names = set() if not self.params else set(self.params.keys())
        # NOTE(al-maisan) Do we have all the mandatory params?
        if not api_info.mandatory.issubset(param_names):
            missing = sorted(api_info.mandatory - param_names)
            return "Missing mandatory params: '%s'" % ', '.join(missing)

        # NOTE(al-maisan) Our params must be either in the mandatory or the
        # optional subset.
        all_permissible_params = api_info.mandatory.union(api_info.optional)
        if not param_names.issubset(all_permissible_params):
            invalid = sorted(param_names - all_permissible_params)
            return "Invalid params: '%s'" % ', '.join(invalid)

        return None
