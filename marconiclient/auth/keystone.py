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

from oslo.config import cfg

from keystoneclient.v2_0 import client as ksclient

from marconiclient.auth import base
from marconiclient.common import utils


# NOTE(flaper87): Some of the code below
# was brought to you by the very unique
# work of ceilometerclient.
class KeystoneAuth(base.AuthBackend):

    _CLI_OPTIONS = [
        cfg.StrOpt("os_username", default=utils.env('OS_USERNAME'),
                   help='Defaults to env[OS_USERNAME]'),

        cfg.StrOpt("os_password", default=utils.env('OS_PASSWORD'),
                   help='Defaults to env[OS_PASSWORD]'),

        cfg.StrOpt("os_project_id", default=utils.env('OS_PROJECT_ID'),
                   help='Defaults to env[OS_PROJECT_ID]'),

        cfg.StrOpt("os_project_name", default=utils.env('OS_PROJECT_NAME'),
                   help='Defaults to env[OS_PROJECT_NAME]'),

        cfg.StrOpt("os_auth_url", default=utils.env('OS_AUTH_URL'),
                   help='Defaults to env[OS_AUTH_URL]'),

        cfg.StrOpt("os_auth_token", default=utils.env('OS_AUTH_TOKEN'),
                   help='Defaults to env[OS_AUTH_TOKEN]'),

        cfg.StrOpt("os_region_name", default=utils.env('OS_REGION_NAME'),
                   help='Defaults to env[OS_REGION_NAME]'),

        cfg.StrOpt("os_service_type", default=utils.env('OS_SERVICE_TYPE'),
                   help='Defaults to env[OS_SERVICE_TYPE]'),

        cfg.StrOpt("os_service_type", default=utils.env('OS_SERVICE_TYPE'),
                   help='Defaults to env[OS_SERVICE_TYPE]'),

        cfg.StrOpt("os_endpoint_type", default=utils.env('OS_ENDPOINT_TYPE'),
                   help='Defaults to env[OS_ENDPOINT_TYPE]'),

    ]

    def __init__(self, conf):
        super(KeystoneAuth, self).__init__(conf)
        conf.register_cli_opts(self._CLI_OPTIONS)

    def _get_ksclient(self, **kwargs):
        """Get an endpoint and auth token from Keystone.

        :param kwargs: keyword args containing credentials:
                * username: name of user
                * password: user's password
                * auth_url: endpoint to authenticate against
                * insecure: allow insecure SSL (no cert verification)
                * project_{name|id}: name or ID of project
        """
        return ksclient.Client(username=self.conf.os_username,
                               password=self.conf.os_password,
                               tenant_id=self.conf.os_project_id,
                               tenant_name=self.conf.os_project_name,
                               auth_url=self.conf.os_auth_url,
                               insecure=self.conf.insecure)

    def _get_endpoint(self, client):
        """Get an endpoint using the provided keystone client."""
        return client.service_catalog.url_for(
            service_type=self.conf.service_type or 'queuing',
            endpoint_type=self.conf.endpoint_type or 'publicURL')

    def authenticate(self, api_version, request):
        """Get an authtenticated client, based on the credentials
        in the keyword args.

        :param api_version: the API version to use ('1' or '2')
        :param request: The request spec instance to modify with
            the auth information.
        """

        token = self.conf.os_auth_token
        if not self.conf.os_auth_token or not request.endpoint:
            # NOTE(flaper87): Lets assume all the
            # required information was provided
            # either through env variables or CLI
            # params. Let keystoneclient fail otherwise.
            ks_kwargs = {
                'username': self.conf.os_username,
                'password': self.conf.os_password,
                'tenant_id': self.conf.os_project_id,
                'tenant_name': self.conf.os_project_name,
                'auth_url': self.conf.os_auth_url,
                'service_type': self.conf.os_service_type,
                'endpoint_type': self.conf.os_endpoint_type,
                'insecure': self.conf.insecure,
            }

            _ksclient = self._get_ksclient(**ks_kwargs)

            if not token:
                token = _ksclient.auth_token

            if not request.endpoint:
                request.endpoint = self._get_endpoint(_ksclient, **ks_kwargs)

        # NOTE(flaper87): Update the request spec
        # with the final token.
        request.headers['X-Auth-Token'] = token
        return request
