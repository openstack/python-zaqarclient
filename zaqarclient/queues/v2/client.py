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
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import flavor
from zaqarclient.queues.v2 import iterator
from zaqarclient.queues.v2 import pool
from zaqarclient.queues.v2 import queues
from zaqarclient.queues.v2 import subscription
from zaqarclient import transport
from zaqarclient.transport import request


class Client(object):
    """Client base class

    :param url: Zaqar's instance base url.
    :type url: str
    :param version: API Version pointing to.
    :type version: `int`
    :param conf: CONF object.
    :type conf: `oslo_config.cfg.CONF`
    """

    queues_module = queues

    def __init__(self, url=None, version=2, conf=None, session=None):
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

        return transport.get_transport_for(request,
                                           version=self.api_version,
                                           options=self.conf)

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
                                           version=self.api_version)

    def queue(self, ref, **kwargs):
        """Returns a queue instance

        :param ref: Queue's reference id.
        :type ref: str

        :returns: A queue instance
        :rtype: `queues.Queue`
        """
        return queues.Queue(self, ref, **kwargs)

    def queues(self, **params):
        """Gets a list of queues from the server

        :returns: A list of queues
        :rtype: `list`
        """
        req, trans = self._request_and_transport()

        queue_list = core.queue_list(trans, req, **params)

        count = None
        if params.get("with_count"):
            count = queue_list.get("count", None)

        list_iter = iterator._Iterator(self, queue_list, 'queues',
                                       self.queues_module.create_object(self))
        return (list_iter, count)

    def follow(self, ref):
        """Follows ref.

        This method instanciates a new request instance and requests
        `ref`. It is intended to be used to follow a reference href
        gotten from `links` sections in responses like queues' lists.

        :params ref: The reference path.
        :type ref: str
        """
        req, trans = self._request_and_transport()
        req.ref = ref

        return trans.send(req).deserialized_content

    # ADMIN API
    def pool(self, ref, **kwargs):
        """Returns a pool instance

        :param ref: Pool's reference name.
        :type ref: str

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

    def flavor(self, ref, **kwargs):
        """Returns a flavor instance

        :param ref: Flavor's reference name.
        :type ref: str

        :returns: A flavor instance
        :rtype: `flavor.Flavor`
        """
        return flavor.Flavor(self, ref, **kwargs)

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

    def subscription(self, queue_name, **kwargs):
        """Returns a subscription instance

        :param queue_name: Name of the queue to subscribe to.
        :type queue_name: str

        :returns: A subscription instance
        :rtype: `subscription.Subscription`
        """
        return subscription.Subscription(self, queue_name, **kwargs)

    def subscriptions(self, queue_name, **params):
        """Gets a list of subscriptions from the server

        :param params: Filters to use for getting subscriptions
        :type params: dict.

        :returns: A list of subscriptions
        :rtype: `list`
        """
        req, trans = self._request_and_transport()

        subscription_list = core.subscription_list(trans, req, queue_name,
                                                   **params)

        return iterator._Iterator(self,
                                  subscription_list,
                                  'subscriptions',
                                  subscription.create_object(self))

    def ping(self):
        """Gets the health status of Zaqar server."""
        req, trans = self._request_and_transport()
        return core.ping(trans, req)

    def health(self):
        """Gets the detailed health status of Zaqar server."""
        req, trans = self._request_and_transport()
        return core.health(trans, req)

    def homedoc(self):
        """Get the detailed resource doc of Zaqar server"""
        req, trans = self._request_and_transport()
        return core.homedoc(trans, req)
