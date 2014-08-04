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

from keystoneclient.v2_0 import client as ksclient

from zaqarclient.auth import base


# NOTE(flaper87): Some of the code below
# was brought to you by the very unique
# work of ceilometerclient.
class KeystoneAuth(base.AuthBackend):
    """Keystone Auth backend

    :params conf: A dictionary with Keystone's
        custom parameters:
            - os_username
            - os_password
            - os_project_id
            - os_project_name
            - os_auth_url
            - os_auth_token
            - os_region_name
            - os_service_type
            - os_service_type
            - os_endpoint_type
    :type conf: `dict`
    """

    def _get_ksclient(self, **kwargs):
        """Get an endpoint and auth token from Keystone.

        :param kwargs: keyword args containing credentials:
                * username: name of user
                * password: user's password
                * auth_url: endpoint to authenticate against
                * insecure: allow insecure SSL (no cert verification)
                * project_{name|id}: name or ID of project
        """
        return ksclient.Client(**kwargs)

    def _get_endpoint(self, client, **extra):
        """Get an endpoint using the provided keystone client."""
        return client.service_catalog.url_for(**extra)

    def authenticate(self, api_version, request):
        """Get an authtenticated client, based on the credentials
        in the keyword args.

        :param api_version: the API version to use ('1' or '2')
        :param request: The request spec instance to modify with
            the auth information.
        """

        token = self.conf.get('os_auth_token')
        if not token or not request.endpoint:
            # NOTE(flaper87): Lets assume all the
            # required information was provided
            # either through env variables or CLI
            # params. Let keystoneclient fail otherwise.
            ks_kwargs = {
                'username': self.conf.get('os_username'),
                'password': self.conf.get('os_password'),
                'tenant_id': self.conf.get('os_project_id'),
                'tenant_name': self.conf.get('os_project_name'),
                'auth_url': self.conf.get('os_auth_url'),
                'insecure': self.conf.get('insecure'),
            }

            _ksclient = self._get_ksclient(**ks_kwargs)

            if not token:
                token = _ksclient.auth_token

            if not request.endpoint:
                extra = {
                    'service_type': self.conf.get('os_service_type',
                                                  'queuing'),
                    'endpoint_type': self.conf.get('os_endpoint_type',
                                                   'publicURL'),
                }
                request.endpoint = self._get_endpoint(_ksclient, **extra)

        # NOTE(flaper87): Update the request spec
        # with the final token.
        request.headers['X-Auth-Token'] = token
        return request
