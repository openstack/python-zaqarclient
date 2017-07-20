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
from zaqarclient.queues.v1 import client
from zaqarclient.queues.v1 import iterator
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import queues
from zaqarclient.queues.v2 import subscription


class Client(client.Client):
    """Client base class

    :param url: Zaqar's instance base url.
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

    queues_module = queues

    def __init__(self, url=None, version=2, conf=None, session=None):
        self.conf = conf or {}

        self.api_url = url
        self.api_version = version
        self.auth_opts = self.conf.get('auth_opts', {})
        self.client_uuid = self.conf.get('client_uuid',
                                         uuidutils.generate_uuid(dashed=False))
        self.session = session

    def queue(self, ref, **kwargs):
        """Returns a queue instance

        :param ref: Queue's reference id.
        :type ref: `six.text_type`

        :returns: A queue instance
        :rtype: `queues.Queue`
        """
        return queues.Queue(self, ref, **kwargs)

    @decorators.version(min_version=2)
    def subscription(self, queue_name, **kwargs):
        """Returns a subscription instance

        :param queue_name: Name of the queue to subscribe to.
        :type queue_name: `six.text_type`

        :returns: A subscription instance
        :rtype: `subscription.Subscription`
        """
        return subscription.Subscription(self, queue_name, **kwargs)

    @decorators.version(min_version=2)
    def subscriptions(self, queue_name, **params):
        """Gets a list of subscriptions from the server

        :param params: Filters to use for getting subscriptions
        :type params: **kwargs dict.

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

    @decorators.version(min_version=1.1)
    def health(self):
        """Gets the detailed health status of Zaqar server."""
        req, trans = self._request_and_transport()
        return core.health(trans, req)

    @decorators.version(min_version=1.1)
    def homedoc(self):
        """Get the detailed resource doc of Zaqar server"""
        req, trans = self._request_and_transport()
        return core.homedoc(trans, req)
