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

from oslo.config import cfg
import six
from six.moves.urllib import parse
from stevedore import driver

from marconiclient import errors as _errors

_TRANSPORT_OPTIONS = [
    cfg.StrOpt('default_transport', default='http',
               help='Transport to use as default'),
    cfg.IntOpt('default_transport_version', default=1,
               help='Transport to use as default'),
]


def get_transport(conf, transport, version=1):
    """Gets a transport and returns it.

    :param conf: the user configuration
    :type conf: cfg.ConfigOpts
    :param transport: Transport name
    :type transport: `six.string_types`
    :param version: Version of the target transport.
    :type version: int

    :returns: A `Transport` instance.
    :rtype: `marconiclient.transport.Transport`
    """

    entry_point = '{0}.v{1}'.format(transport, version)

    try:
        namespace = 'marconiclient.transport'
        mgr = driver.DriverManager(namespace,
                                   entry_point,
                                   invoke_on_load=True,
                                   invoke_args=[conf])
    except RuntimeError as ex:
        raise _errors.DriverLoadFailure(entry_point, ex)

    return mgr.driver


def get_transport_for_conf(conf):
    """Gets a transport based on the config object

    It'll load a transport based on the `default-transport`
    and `default-transport-version` params.

    :param conf: the user configuration
    :type conf: cfg.ConfigOpts
    """
    conf.register_opts(_TRANSPORT_OPTIONS)
    return get_transport(conf, conf.default_transport,
                         conf.default_transport_version)


def get_transport_for(conf, url_or_request, version=1):
    """Gets a transport for a given url.

    An example transport URL might be::

        zmq://example.org:8888/v1/

    :param conf: the user configuration
    :type conf: cfg.ConfigOpts
    :param url_or_request: a transport URL
    :type url_or_request: `six.string_types` or
        `marconiclient.transport.request.Request`
    :param version: Version of the target transport.
    :type version: int

    :returns: A `Transport` instance.
    :rtype: `marconiclient.transport.Transport`
    """

    url = url_or_request
    if not isinstance(url_or_request, six.string_types):
        url = url_or_request.endpoint

    parsed = parse.urlparse(url)
    return get_transport(conf, parsed.scheme, version)
