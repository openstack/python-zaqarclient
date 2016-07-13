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

import abc

import six

from zaqarclient.transport import errors


@six.add_metaclass(abc.ABCMeta)
class Transport(object):

    # common HTTP codes used by multiple transports
    http_to_zaqar = {
        400: errors.MalformedRequest,
        401: errors.UnauthorizedError,
        403: errors.ForbiddenError,
        404: errors.ResourceNotFound,
        409: errors.ConflictError,
        500: errors.InternalServerError,
        503: errors.ServiceUnavailableError
    }

    def __init__(self, options):
        self.options = options

    @abc.abstractmethod
    def send(self, request):
        """Returns the response.

        :returns: The final response
        :rtype: `zaqarclient.transport.response.Response`
        """
