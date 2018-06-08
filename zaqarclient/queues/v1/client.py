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

from oslo_utils import uuidutils
from zaqarclient.common import decorators
from zaqarclient.queues.v1 import core
from zaqarclient.queues.v1 import flavor
from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v1 import pool
from zaqarclient.queues.v1 import queues
from zaqarclient import transport
from zaqarclient.transport import errors
from zaqarclient.transport import request


class Client(object):
    """Client base class

    :param url: Zaqar's instance base url.
    :type url: `six.text_type`
    :param version: API Version pointing to.
    :type version: `int`
    :param conf: CONF object.
    :type conf: `oslo_config.cfg.CONF`
    :param session: keystone session. But it's just place holder, we wont'
        support it in v1.
    """

    queues_module = queues

    def __init__(self, url=None, version=1, conf=None, session=None):
        self.conf = conf or {}

        self.api_url = url
        self.api_version = version
        self.auth_opts = self.conf.get('auth_opts', {})
        self.client_uuid = self.conf.get('client_uuid',
                                         uuidutils.generate_uuid(dashed=False))
        self.session = session

    def _get_transport(self, request):
        """Gets a transport and caches its instance

        This method gets a transport instance based on
        the request's endpoint and caches that for later
        use. The transport instance is invalidated whenever
        a session expires.

        :param request: The request to use to load the
            transport instance.
        :type request: :class:`zaqarclient.transport.request.Request`
        """

        trans = transport.get_transport_for(request,
                                            options=self.conf)
        return (trans or self.transport)

    def _request_and_transport(self):
        req = request.prepare_request(self.auth_opts,
                                      endpoint=self.api_url,
                                      api=self.api_version,
                                      session=self.session)

        req.headers['Client-ID'] = self.client_uuid

        trans = self._get_transport(req)
        return req, trans

    def transport(self):
        """Gets a transport based the api url and version.

        :rtype: :class:`zaqarclient.transport.base.Transport`
        """
        return transport.get_transport_for(self.api_url,
                                           self.api_version)

    def queue(self, ref, **kwargs):
        """Returns a queue instance

        :param ref: Queue's reference id.
        :type ref: `six.text_type`

        :returns: A queue instance
        :rtype: `queues.Queue`
        """
        return self.queues_module.Queue(self, ref, **kwargs)

    def queues(self, **params):
        """Gets a list of queues from the server

        :returns: A list of queues
        :rtype: `list`
        """
        req, trans = self._request_and_transport()

        queue_list = core.queue_list(trans, req, **params)

        return iterator._Iterator(self,
                                  queue_list,
                                  'queues',
                                  self.queues_module.create_object(self))

    def follow(self, ref):
        """Follows ref.

        This method instanciates a new request instance and requests
        `ref`. It is intended to be used to follow a reference href
        gotten from `links` sections in responses like queues' lists.

        :params ref: The reference path.
        :type ref: `six.text_type`
        """
        req, trans = self._request_and_transport()
        req.ref = ref

        return trans.send(req).deserialized_content

    # ADMIN API
    def pool(self, ref, **kwargs):
        """Returns a pool instance

        :param ref: Pool's reference name.
        :type ref: `six.text_type`

        :returns: A pool instance
        :rtype: `pool.Pool`
        """
        return pool.Pool(self, ref, **kwargs)

    def pools(self, **params):
        """Gets a list of pools from the server

        :param params: Filters to use for getting pools
        :type params: dict.

        :returns: A list of pools
        :rtype: `list`
        """
        req, trans = self._request_and_transport()

        pool_list = core.pool_list(trans, req, **params)

        return iterator._Iterator(self,
                                  pool_list,
                                  'pools',
                                  pool.create_object(self))

    @decorators.version(min_version=1.1)
    def flavor(self, ref, **kwargs):
        """Returns a flavor instance

        :param ref: Flavor's reference name.
        :type ref: `six.text_type`

        :returns: A flavor instance
        :rtype: `flavor.Flavor`
        """
        return flavor.Flavor(self, ref, **kwargs)

    @decorators.version(min_version=1.1)
    def flavors(self, **params):
        """Gets a list of flavors from the server

        :param params: Filters to use for getting flavors
        :type params: dict.

        :returns: A list of flavors
        :rtype: `list`
        """
        req, trans = self._request_and_transport()

        flavor_list = core.flavor_list(trans, req, **params)

        return iterator._Iterator(self,
                                  flavor_list,
                                  'flavors',
                                  flavor.create_object(self))

    def health(self):
        """Gets the health status of Zaqar server."""
        req, trans = self._request_and_transport()
        try:
            core.health(trans, req)
            return True
        except errors.ServiceUnavailableError:
            return False
