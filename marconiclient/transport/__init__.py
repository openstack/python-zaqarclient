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

import six
from six.moves.urllib import parse
from stevedore import driver

from marconiclient import errors


class DriverLoadFailure(errors.MarconiError):
    """Raised if a transport driver can't be loaded."""

    def __init__(self, driver, ex):
        msg = 'Failed to load transport driver "%s": %s' % (driver, ex)
        super(DriverLoadFailure, self).__init__(msg)
        self.driver = driver
        self.ex = ex


def get_transport(conf, url_or_request, module='queues'):
    """Gets a transport for a given url.

    An example transport URL might be::

        zmq://example.org:8888/v1/

    :param conf: the user configuration
    :type conf: cfg.ConfigOpts
    :param url_or_request: a transport URL
    :type url_or_request: `six.string_types` or
        `marconiclient.transport.request.Request`
    :param module: Module the target transport belongs to.
    :type module: str

    :returns: A `Transport` instance.
    :rtype: `marconiclient.transport.Transport`
    """

    url = url_or_request
    if not isinstance(url_or_request, six.string_types):
        url = url_or_request.endpoint

    parsed = parse.urlparse(url)

    try:
        namespace = 'marconiclient.{0}.transport'.format(module)
        mgr = driver.DriverManager(namespace,
                                   parsed.scheme,
                                   invoke_on_load=True,
                                   invoke_args=[conf])
    except RuntimeError as ex:
        raise DriverLoadFailure(parsed.scheme, ex)

    return mgr.driver
