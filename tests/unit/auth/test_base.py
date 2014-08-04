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

from zaqarclient import auth
from zaqarclient.tests import base


class TestBaseAuth(base.TestBase):

    def test_get_backend(self):
        try:
            auth.get_backend(options=self.conf)
        except KeyError:
            self.fail("Test failed")

    def test_get_non_existing_backend(self):
        try:
            auth.get_backend('not_existing')
            self.fail("Test failed")
        except KeyError:
            pass
