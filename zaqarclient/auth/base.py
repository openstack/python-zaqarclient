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

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class AuthBackend(object):

    def __init__(self, conf):
        self.conf = conf

    @abc.abstractmethod
    def authenticate(self, api_version, request):
        """Authenticates the user in the selected backend.

        Auth backends will have to manipulate the
        request and prepare it to send the auth information
        back to Zaqar's instance.

        :params api_version: Zaqar's API version.
        :params request: Request Spec instance
            that can be manipulated by the backend
            if the authentication succeeds.

        :returns: The modified request spec.
        """


class NoAuth(AuthBackend):
    """No Auth Plugin."""

    def authenticate(self, api_version, req):
        return req
