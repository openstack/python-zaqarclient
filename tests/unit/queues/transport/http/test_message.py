# Copyright (c) 2013 Rackspace, Inc.
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
import unittest

import mock

from marconiclient.queues.transport.http import message
from marconiclient.tests.mock import message as mock_message


HREF = '/v1/queue/dgq/messages/my_msg_is_chocolate'
AGE = 100
TTL = 120


class TestSimpleMessage(unittest.TestCase):
    def setUp(self):
        msg_body = {
            'href': HREF,
            'ttl': TTL,
            'age': AGE,
            'body': {'name': 'chocolate'}
        }
        self.conn = mock.MagicMock()
        self.msg = message.from_dict(msg_body, connection=self.conn)

    def _attr_check(self, xhref, xttl, xage, xbody):
        self.assertEqual(self.msg.href, xhref)
        self.assertEqual(self.msg.ttl, xttl)
        self.assertEqual(self.msg.age, xage)
        self.assertEqual(self.msg.body, xbody)

    def test_attributes_match_expected(self):
        self._attr_check(xhref=HREF, xttl=TTL, xage=AGE,
                         xbody={'name': 'chocolate'})

    def test_repr_matches_expected(self):
        self.assertEqual(repr(self.msg),
                         '<Message ttl:%s>' % (self.msg.ttl,))

    def test_delete_works(self):
        self.msg.delete()

    def test_reload_works(self):
        msg = mock_message.message(
            href=HREF, ttl=TTL - 1, age=AGE + 1,
            body={'name': 'vanilla'})
        self.conn.get.return_value = mock.MagicMock()
        self.conn.get.return_value.json.return_value = msg
        self.msg.reload()
        self._attr_check(xhref=HREF, xttl=TTL - 1, xage=AGE + 1,
                         xbody={'name': 'vanilla'})

    def test_reload_after_delete_throws(self):
        self.msg.delete()
        self.assertRaises(AssertionError, self.msg.reload)

    def test_delete_after_delete_throws(self):
        self.msg.delete()
        self.assertRaises(AssertionError, self.msg.delete)
