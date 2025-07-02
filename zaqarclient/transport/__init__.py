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

import urllib.parse

from stevedore import driver

from zaqarclient import errors as _errors


def get_transport(transport='http', version=2, options=None):
    """Gets a transport and returns it.

    :param transport: Transport name.
        Default: http
    :type transport: str
    :param version: Version of the target transport.
        Default: 2
    :type version: int

    :returns: A `Transport` instance.
    :rtype: `zaqarclient.transport.Transport`
    """

    entry_point = '{0}.v{1}'.format(transport, version)

    try:
        namespace = 'zaqarclient.transport'
        mgr = driver.DriverManager(namespace,
                                   entry_point,
                                   invoke_on_load=True,
                                   invoke_args=[options])
    except RuntimeError as ex:
        raise _errors.DriverLoadFailure(entry_point, ex)

    return mgr.driver


def get_transport_for(url_or_request, version=2, options=None):
    """Gets a transport for a given url.

    An example transport URL might be::

        zmq://example.org:8888/v2/

    :param url_or_request: a transport URL
    :type url_or_request: str or
        `zaqarclient.transport.request.Request`
    :param version: Version of the target transport.
        Default: 2
    :type version: int

    :returns: A `Transport` instance.
    :rtype: `zaqarclient.transport.Transport`
    """

    url = url_or_request
    if not isinstance(url_or_request, str):
        url = url_or_request.endpoint

    parsed = urllib.parse.urlparse(url)
    return get_transport(parsed.scheme, version, options)
