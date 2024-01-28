# Copyright (c) 2013  Red Hat, Inc.
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

import os
import urllib.parse

import fixtures
import openstack.config
import testtools

_USE_AUTHENTICATION = os.environ.get('ZAQARCLIENT_AUTH_FUNCTIONAL', False)
_RUN_FUNCTIONAL = os.environ.get('ZAQARCLIENT_TEST_FUNCTIONAL',
                                 _USE_AUTHENTICATION)


class TestBase(testtools.TestCase):

    transport_cls = None
    is_functional = False

    def setUp(self):
        super(TestBase, self).setUp()

        self.conf = {
            'auth_opts': {
                'backend': 'noauth',
                'options': {
                    'os_project_id': 'my-project'
                }
            }
        }
        self.useFixture(fixtures.FakeLogger('zaqar'))

        # NOTE(kgriffs): Don't monkey-patch stdout since it breaks
        # debugging with pdb.
        stderr = self.useFixture(fixtures.StringStream('stderr')).stream
        self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        if not _RUN_FUNCTIONAL and self.is_functional:
            self.skipTest('Functional tests disabled')
        elif self.is_functional and _USE_AUTHENTICATION:
            self._setup_auth_params()

    def _credentials(self, cloud='devstack-admin'):
        """Retrieves credentials to run functional tests

        Credentials are either read via os-client-config from the environment
        or from a config file ('clouds.yaml'). Environment variables override
        those from the config file.

        devstack produces a clouds.yaml with two named clouds - one named
        'devstack' which has user privs and one named 'devstack-admin' which
        has admin privs. This function will default to getting the
        devstack-admin cloud as that is the current expected behavior.
        """
        os_cfg = openstack.config.OpenStackConfig()
        try:
            found = os_cfg.get_one_cloud(cloud=cloud)
        except Exception:
            found = os_cfg.get_one_cloud()
        return found

    def _setup_auth_params(self):
        self.creds = self._credentials().get_auth_args()

        parsed_url = urllib.parse.urlparse(self.creds['auth_url'])
        auth_url = self.creds['auth_url']
        if not parsed_url.path or parsed_url.path == '/':
            auth_url = urllib.parse.urljoin(self.creds['auth_url'], 'v3')
        if parsed_url.path == '/identity':
            auth_url = '%s/v3' % auth_url

        self.conf['auth_opts']['backend'] = 'keystone'
        options = {'os_username': self.creds['username'],
                   'os_user_domain_id': self.creds['user_domain_id'],
                   'os_password': self.creds['password'],
                   'os_project_name': self.creds['project_name'],
                   'os_project_id': '',
                   'os_project_domain_id': self.creds['project_domain_id'],
                   'os_auth_url': auth_url}

        self.conf['auth_opts'].setdefault('options', {}).update(options)

    def config(self, group=None, **kw):
        """Override some configuration values.

        The keyword arguments are the names of configuration options to
        override and their values.

        If a group argument is supplied, the overrides are applied to
        the specified configuration option group.
        """
        parent = (group and self.conf.setdefault(group, {}) or
                  self.conf)
        parent.update(kw)
