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

from zaqarclient.queues.v2 import core


class Flavor(object):

    def __init__(self, client, name,
                 pool_list=None, auto_create=True,
                 **kwargs):
        self.client = client

        self.name = name
        self.pool_list = pool_list
        self.capabilities = kwargs.get('capabilities', {})

        if auto_create:
            self.ensure_exists()

    def ensure_exists(self):
        """Ensures pool exists

        This method is not race safe,
        the pool could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()
        # As of now on PUT, zaqar server updates flavor if it is already
        # exists else it will create a new one. The zaqar client should
        # maitain symmetry with zaqar server.
        # TBD(mdnadeem): Have to change this code when zaqar server
        # behaviour change for PUT operation.

        data = {'pool_list': self.pool_list}

        req, trans = self.client._request_and_transport()
        core.flavor_create(trans, req, self.name, data)

    def update(self, flavor_data):
        req, trans = self.client._request_and_transport()
        core.flavor_update(trans, req, self.name, flavor_data)

        for key, value in flavor_data.items():
            setattr(self, key, value)

    def delete(self):
        req, trans = self.client._request_and_transport()
        core.flavor_delete(trans, req, self.name)

    def get(self):
        req, trans = self.client._request_and_transport()
        return core.flavor_get(trans, req, self.name, callback=None)


def create_object(parent):
    return lambda kwargs: Flavor(parent, kwargs.pop('name'),
                                 auto_create=False, **kwargs)
