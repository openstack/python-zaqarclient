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

import requests


class Client(object):

    def __init__(self, *args, **kwargs):
        self.session = requests.session(*args, **kwargs)

    def request(self, *args, **kwargs):
        """Raw request."""
        return self.session.request(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Does  http GET."""
        return self.session.get(*args, **kwargs)

    def head(self, *args, **kwargs):
        """Does  http HEAD."""
        return self.session.head(*args, **kwargs)

    def option(self, *args, **kwargs):
        """Does  http OPTION."""
        return self.session.option(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Does  http POST."""

        if "data" in kwargs:
            kwargs['data'] = json.dumps(kwargs["data"])

        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Does  http PUT."""

        if "data" in kwargs:
            kwargs['data'] = json.dumps(kwargs["data"])

        return self.session.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Does  http DELETE."""
        return self.session.delete(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Does  http PATCH."""
        if "data" in kwargs:
            kwargs['data'] = json.dumps(kwargs["data"])
        return self.session.patch(*args, **kwargs)
