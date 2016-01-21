# Copyright (c) 2016 Red Hat, Inc.
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


class SignedURLAuth(base.AuthBackend):
    """Authenticate using signature.

    The returned client will only work on one dedicated queue which has been
    signed.

    :params conf: A dictionary with the signed URL data:
            - expires
            - methods
            - paths
            - signature
            - os_project_id
    :type conf: `dict`
    """

    def authenticate(self, api_version, request):
        """Set the necessary headers on the request."""
        request.headers['URL-Expires'] = self.conf['expires']
        request.headers['URL-Methods'] = ','.join(self.conf['methods'])
        request.headers['URL-Paths'] = ','.join(self.conf['paths'])
        request.headers['URL-Signature'] = self.conf['signature']
        return request
