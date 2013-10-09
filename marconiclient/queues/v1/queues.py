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

from marconiclient.queues.v1 import core
from marconiclient import transport
from marconiclient.transport import request


class Queue(object):

    def __init__(self, client, queue_id, auto_create=True):
        self.client = client

        # NOTE(flaper87) Queue Info
        self._id = queue_id
        self._metadata = None

        if auto_create:
            self.ensure_exists()

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

        trans = transport.get_transport_for(self.client.conf, request)
        return (trans or self.client.transport)

    def _request_and_transport(self):
        api = 'queues.v' + str(self.client.api_version)
        req = request.prepare_request(self.client.conf,
                                      endpoint=self.client.api_url,
                                      api=api)

        trans = self._get_transport(req)
        return req, trans

    def exists(self):
        """Checks if the queue exists."""
        req, trans = self._request_and_transport()
        return core.queue_exists(trans, req, self._id)

    def ensure_exists(self):
        """Ensures a queue exists

        This method is not race safe,
        the queue could've been deleted
        right after it was called.
        """
        req, trans = self._request_and_transport()
        core.queue_create(trans, req, self._id)

    def metadata(self, new_meta=None, force_reload=False):
        """Get metadata and return it

        :param new_meta: A dictionary containing
            an updated metadata object. If present
            the queue metadata will be updated in
            remote server.
        :type new_meta: `dict`
        :param force_reload: Whether to ignored the
            cached metadata and reload it from the
            server.
        :type force_reload: `bool`

        :returns: The queue metadata.
        """
        req, trans = self._request_and_transport()

        if new_meta:
            core.queue_set_metadata(trans, req, self._id, new_meta)
            self._metadata = new_meta

        # TODO(flaper87): Cache with timeout
        if self._metadata and not force_reload:
            return self._metadata

        self._metadata = core.queue_get_metadata(trans, req, self._id)
        return self._metadata

    def delete(self):
        req, trans = self._request_and_transport()
        core.queue_delete(trans, req, self._id)
