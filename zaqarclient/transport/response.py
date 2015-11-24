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

import json


class Response(object):
    """Common response class for Zaqarclient.

    All `zaqarclient.transport.base.Transport` implementations
    will return this to the higher level API which will then build
    an object out of it.

    :param request: The request sent to the server.
    :type: `zaqarclient.transport.request.Request`
    :param content: Response's content
    :type: `six.string_types`
    :param headers: Optional headers returned in the response.
    :type: dict
    :param status_code: Optional status_code returned in the response.
    :type: `int`
    """

    __slots__ = ('request', 'content', 'headers', 'status_code',
                 '_deserialized')

    def __init__(self, request, content, headers=None, status_code=None):
        self.request = request
        self.content = content
        self.headers = headers or {}
        self.status_code = status_code

        self._deserialized = None

    @property
    def deserialized_content(self):
        try:
            if not self._deserialized and self.content:
                self._deserialized = json.loads(self.content)
            return self._deserialized
        except ValueError as ex:
            print("Response is not a JSON object.", ex)
        return None
