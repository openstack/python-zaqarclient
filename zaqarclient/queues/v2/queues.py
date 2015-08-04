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

from zaqarclient import errors
from zaqarclient.queues.v1 import queues
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import message


class Queue(queues.Queue):

    def message(self, message_id):
        """Gets a message by id

        :param message_id: Message's reference
        :type message_id: `six.text_type`

        :returns: A message
        :rtype: `dict`
        """
        req, trans = self.client._request_and_transport()
        if self.client.api_version >= 2:
            raise errors.InvalidOperation("Unavailable on versions >= 2")
        else:
            msg = core.message_get(trans, req, self._name,
                                   message_id)
            return message.Message(self, **msg)
