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
errors to Marconi errors. For example, HTTP 404s should be
raised as `ResourceNotFound`
"""

from marconiclient import errors

__all__ = ['TransportError', 'ResourceNotFound', 'MalformedRequest']


class TransportError(errors.MarconiError):
    """Base class for all transport errors."""


class ResourceNotFound(TransportError):
    """Indicates that a resource is missing

    This error maps to HTTP's 404
    """


class MalformedRequest(TransportError):
    """Indicates that a request is malformed

    This error maps to HTTP's 400
    """
