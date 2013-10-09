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
This module defines a lower level API for queues' v1. This level of the
API is responsible for packing up the final request, sending it to the server
and handling asynchronous requests.

Functions present in this module assume that:

    1. The transport instance is ready to `send` the
    request to the server.

    2. Transport instance holds the conf instance to use for this
    request.
"""

import json

import marconiclient.transport.errors as errors


def _common_queue_ops(operation, transport, request, name, callback=None):
    """Function for common operation

    This is a lower level call to get a single
    instance of queue.

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: `six.text_type`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """
    request.operation = operation
    request.params['queue_name'] = name
    return transport.send(request)


def queue_create(transport, request, name, callback=None):
    """Creates a queue."""
    return _common_queue_ops('queue_create', transport,
                             request, name, callback=callback)


def queue_exists(transport, request, name, callback=None):
    """Checks if the queue exists."""
    try:
        _common_queue_ops('queue_exists', transport,
                          request, name, callback=callback)
        return True
    except errors.ResourceNotFound:
        return False


def queue_get_metadata(transport, request, name, callback=None):
    """Gets queue metadata."""
    resp = _common_queue_ops('queue_get_metadata', transport,
                             request, name, callback=callback)
    return json.loads(resp.content)


def queue_set_metadata(transport, request, name, metadata, callback=None):
    """Sets queue metadata."""

    request.operation = 'queue_set_metadata'
    request.params['queue_name'] = name
    request.content = json.dumps(metadata)

    transport.send(request)


def queue_delete(transport, request, name, callback=None):
    """Deletes queue."""
    return _common_queue_ops('queue_delete', transport,
                             request, name, callback=callback)
