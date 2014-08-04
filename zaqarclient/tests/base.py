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

import fixtures
import testtools

_RUN_FUNCTIONAL = os.environ.get('ZAQARCLIENT_TEST_FUNCTIONAL', False)


class TestBase(testtools.TestCase):

    transport_cls = None
    is_functional = False

    def setUp(self):
        super(TestBase, self).setUp()

        self.conf = {}
        self.useFixture(fixtures.FakeLogger('zaqar'))

        # NOTE(kgriffs): Don't monkey-patch stdout since it breaks
        # debugging with pdb.
        stderr = self.useFixture(fixtures.StringStream('stderr')).stream
        self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        if not _RUN_FUNCTIONAL and self.is_functional:
            self.skipTest('Functional tests disabled')

    def config(self, group=None, **kw):
        """Override some configuration values.

        The keyword arguments are the names of configuration options to
        override and their values.

        If a group argument is supplied, the overrides are applied to
        the specified configuration option group.
        """
        parent = (group and self.conf.setdefault(group, {})
                  or self.conf)
        parent.update(kw)
