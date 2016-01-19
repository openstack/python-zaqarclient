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

from zaqarclient.queues.v1 import queues
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import message


class Queue(queues.Queue):

    message_module = message

    def signed_url(self, paths=None, ttl_seconds=None, methods=None):
        req, trans = self.client._request_and_transport()
        return core.signed_url_create(trans, req, self._name, paths=paths,
                                      ttl_seconds=ttl_seconds, methods=methods)

    def subscriptions(self, detailed=False, marker=None, limit=20):
        return self.client.subscriptions(queue_name=self._name,
                                         detailed=detailed,
                                         marker=marker,
                                         limit=limit)


def create_object(parent):
    return lambda args: Queue(parent, args["name"], auto_create=False)
