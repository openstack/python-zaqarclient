# Copyright (c) 2014 Red Hat, Inc.
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

from zaqarclient.queues.v1 import core


class Pool(object):

    def __init__(self, client, name,
                 weight=None, uri=None,
                 flavor=None, auto_create=True,
                 **kwargs):
        self.client = client
        self.uri = uri
        self.name = name
        self.weight = weight
        self.flavor = flavor
        self.options = kwargs.get("options", {})

        if auto_create:
            self.ensure_exists()

    def ensure_exists(self):
        """Ensures pool exists

        This method is not race safe,
        the pool could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()
        # As of now on PUT, zaqar server updates pool if it is already
        # exists else it will create a new one. The zaqar client should
        # maitain symmetry with zaqar server.
        # TBD(mdnadeem): Have to change this code when zaqar server
        # behaviour change for PUT operation.

        data = {'uri': self.uri,
                'weight': self.weight,
                'options': self.options}

        if self.client.api_version >= 1.1 and self.flavor:
            data['flavor'] = self.flavor

        req, trans = self.client._request_and_transport()
        core.pool_create(trans, req, self.name, data)

    def update(self, pool_data):
        req, trans = self.client._request_and_transport()
        core.pool_update(trans, req, self.name, pool_data)

        for key, value in pool_data.items():
            setattr(self, key, value)

    def delete(self):
        req, trans = self.client._request_and_transport()
        core.pool_delete(trans, req, self.name)

    def get(self):
        req, trans = self.client._request_and_transport()
        return core.pool_get(trans, req, self.name, callback=None)


def create_object(parent):
    return lambda kwargs: Pool(parent, kwargs.pop('name'),
                               auto_create=False, **kwargs)
