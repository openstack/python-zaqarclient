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
from zaqarclient.transport import errors


class Flavor(object):

    def __init__(self, client, name,
                 pool=None, auto_create=True,
                 **capabilities):
        self.client = client

        self.name = name
        self.pool = pool
        self.capabilities = capabilities

        if auto_create:
            self.ensure_exists()

    def ensure_exists(self):
        """Ensures pool exists

        This method is not race safe,
        the pool could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()

        try:
            flavor = core.flavor_get(trans, req, self.name)
            self.pool = flavor["pool"]
            self.capabilities = flavor.get("capabilities", {})

        except errors.ResourceNotFound:
            data = {'pool': self.pool,
                    'capabilities': self.capabilities}

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


def create_object(parent):
    return lambda args: Flavor(parent, args["name"], auto_create=False)
