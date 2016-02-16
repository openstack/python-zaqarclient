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


"""
Errors below must be used to translate transport specific
errors to Zaqar errors. For example, HTTP 404s should be
raised as `ResourceNotFound`
"""

from zaqarclient import errors

__all__ = ['TransportError', 'ResourceNotFound', 'MalformedRequest',
           'UnauthorizedError', 'ForbiddenError', 'ServiceUnavailableError',
           'InternalServerError', 'ConflictError']


class TransportError(errors.ZaqarError):
    """Base class for all transport errors."""

    code = None

    def __init__(self, title=None, description=None, text=None):
        msg = 'Error response from Zaqar. Code: {0}.'.format(self.code)
        if title:
            msg += ' Title: {0}.'.format(title)
        if description:
            msg += ' Description: {0}.'.format(description)
        if text:
            msg += ' Text: {0}.'.format(text)
        super(TransportError, self).__init__(msg)


class ResourceNotFound(TransportError):
    """Indicates that a resource is missing

    This error maps to HTTP's 404
    """

    code = 404


class MalformedRequest(TransportError):
    """Indicates that a request is malformed

    This error maps to HTTP's 400
    """

    code = 400


class UnauthorizedError(TransportError):
    """Indicates that a request was not authenticated

    This error maps to HTTP's 401
    """

    code = 401


class ForbiddenError(TransportError):
    """Indicates that a request is forbidden to access the particular resource

    This error maps to HTTP's 403
    """

    code = 403


class InternalServerError(TransportError):
    """Indicates that the server encountered an unexpected situation

    This error maps to HTTP's 500
    """

    code = 500


class ServiceUnavailableError(TransportError):
    """Indicates that the server was unable to service the request

    This error maps to HTTP's 503
    """

    code = 503


class ConflictError(TransportError):
    """Indicates that the server was unable to service the request

    This error maps to HTTP's 409
    """

    code = 409
