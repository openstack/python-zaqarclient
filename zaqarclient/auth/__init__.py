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


from zaqarclient.auth import base
from zaqarclient.auth import keystone
from zaqarclient.auth import signed_url

_BACKENDS = {
    'noauth': base.NoAuth,
    'keystone': keystone.KeystoneAuth,
    'signed-url': signed_url.SignedURLAuth,
}


def get_backend(backend='keystone', options=None):
    """Loads backend `auth_backend`

    :params backend: The backend name to load.
        Default: `keystone`
    :type backend: str
    :param options: Options to pass to the Auth
        backend. Refer to the backend for more info.
    :type options: `dict`
    """
    if options is None:
        options = {}

    backend = _BACKENDS[backend](options)
    return backend
