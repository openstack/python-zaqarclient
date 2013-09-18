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
"""Implements a message controller that understands Marconi messages."""


def _args_from_dict(msg):
    return {
        'href': msg['href'],
        'ttl': msg['ttl'],
        'age': msg['age'],
        'body': msg['body']
    }


def from_dict(msg, connection=None):
    """from_dict(dict, Connection) => Message
    :param msg: A dictionary created by decoding a Marconi message JSON reply
    :param connection: A connection to a Marconi server.
    :raises: KeyError If msg is missing fields
    :raises: TypeError if msg is not a dict.
    """
    return Message(
        connection=connection,
        **_args_from_dict(msg)
    )


class Message(object):
    """A handler for Marconi server Message resources.
    Attributes are only downloaded once - at creation time.
    """
    def __init__(self, href, ttl, age, body, connection):
        self.href = href
        self.ttl = ttl
        self.age = age
        self.body = body
        self._connection = connection
        self._deleted = False

    def __repr__(self):
        return '<Message ttl:%s>' % (self.ttl,)

    def _assert_not_deleted(self):
        assert not self._deleted, 'Already deleted'

    def reload(self):
        """Queries the server and updates all local attributes
        with new values.
        """
        self._assert_not_deleted()
        msg = self._connection.get(self.href).json()

        self.href = msg['href']
        self.ttl = msg['ttl']
        self.age = msg['age']
        self.body = msg['body']

    def delete(self):
        """Deletes this resource from the server, but leaves the local
        object intact.
        """
        self._assert_not_deleted()
        self._connection.delete(self.href)
        self._deleted = True
