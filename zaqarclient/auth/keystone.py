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

from keystoneauth1.identity import v3 as v3_auth
from keystoneauth1 import session

from zaqarclient.auth import base
from zaqarclient import errors


# NOTE(flaper87): Some of the code below
# was brought to you by the very unique
# work of ceilometerclient and glanceclient.
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
            - os_endpoint_type
    :type conf: `dict`
    """

    def _get_keystone_session(self, **kwargs):
        cacert = kwargs.pop('cacert', None)
        cert = kwargs.pop('cert', None)
        key = kwargs.pop('key', None)
        insecure = kwargs.pop('insecure', False)
        auth_url = kwargs.pop('auth_url', None)
        project_id = kwargs.pop('project_id', None)
        project_name = kwargs.pop('project_name', None)
        token = kwargs.get('token')

        if insecure:
            verify = False
        else:
            verify = cacert or True

        if cert and key:
            # passing cert and key together is deprecated in favour of the
            # requests lib form of having the cert and key as a tuple
            cert = (cert, key)

        # create the keystone client session
        ks_session = session.Session(verify=verify, cert=cert)

        username = kwargs.pop('username', None)
        password = kwargs.pop('password', None)
        user_id = kwargs.pop('user_id', None)
        user_domain_name = kwargs.pop('user_domain_name', None)
        user_domain_id = kwargs.pop('user_domain_id', None)
        project_domain_name = kwargs.pop('project_domain_name', None)
        project_domain_id = kwargs.pop('project_domain_id', None)
        auth = None

        if auth_url is None:
            raise errors.ZaqarError(
                'Unable to determine the Keystone endpoint because auth_url '
                'is not given.')

        if token:
            auth = v3_auth.Token(
                auth_url,
                token=token,
                project_name=project_name,
                project_id=project_id,
                project_domain_name=project_domain_name,
                project_domain_id=project_domain_id)
        else:
            auth = v3_auth.Password(
                auth_url,
                username=username,
                password=password,
                user_id=user_id,
                user_domain_name=user_domain_name,
                user_domain_id=user_domain_id,
                project_name=project_name,
                project_id=project_id,
                project_domain_name=project_domain_name,
                project_domain_id=project_domain_id)

        ks_session.auth = auth
        return ks_session

    def _get_endpoint(self, ks_session, **kwargs):
        """Get an endpoint using the provided keystone session."""

        # Set service specific endpoint types
        endpoint_type = kwargs.get('endpoint_type') or 'publicURL'
        service_type = kwargs.get('service_type') or 'messaging'
        region_name = kwargs.get('region_name')

        endpoint = ks_session.get_endpoint(service_type=service_type,
                                           interface=endpoint_type,
                                           region_name=region_name)

        return endpoint

    def authenticate(self, api_version, request):
        """Get an authtenticated client using credentials in the keyword args.

        :param api_version: the API version to use ('1' or '2')
        :param request: The request spec instance to modify with
            the auth information.
        """

        def get_options(k):
            return self.conf.get(k, self.conf.get("os_%s" % k))

        token = get_options('auth_token')
        if not token or not request.endpoint:
            ks_kwargs = {}
            keys = ("username", "password", "project_id",
                    "project_name", "auth_url", "insecure",
                    "cacert", "region_name", "user_domain_name",
                    "user_domain_id", "project_domain_name",
                    "project_domain_id")
            for k in keys:
                ks_kwargs.update({k: get_options(k)})

            ks_session = (request.session or
                          self._get_keystone_session(**ks_kwargs))
            if not token:
                token = ks_session.get_token()
            if not request.endpoint:
                request.endpoint = self._get_endpoint(ks_session, **ks_kwargs)

        # NOTE(flaper87): Update the request spec
        # with the final token.
        request.headers['X-Auth-Token'] = token
        # NOTE(flwang): We also need to apply the insecure and cacert when
        # talking with Zaqar server.
        request.verify = not get_options('insecure')
        request.cert = get_options('cacert')
        return request
