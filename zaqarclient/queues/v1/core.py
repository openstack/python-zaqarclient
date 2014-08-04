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

import zaqarclient.transport.errors as errors


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
    resp = transport.send(request)
    return resp.deserialized_content


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
    return _common_queue_ops('queue_get_metadata', transport,
                             request, name, callback=callback)


def queue_set_metadata(transport, request, name, metadata, callback=None):
    """Sets queue metadata."""

    request.operation = 'queue_set_metadata'
    request.params['queue_name'] = name
    request.content = json.dumps(metadata)

    transport.send(request)


def queue_get_stats(transport, request, name):
    return _common_queue_ops('queue_get_stats', transport,
                             request, name)


def queue_delete(transport, request, name, callback=None):
    """Deletes queue."""
    return _common_queue_ops('queue_delete', transport,
                             request, name, callback=callback)


def queue_list(transport, request, callback=None, **kwargs):
    """Gets a list of queues

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    :param kwargs: Optional arguments for this operation.
        - marker: Where to start getting queues from.
        - limit: Maximum number of queues to get.
    """

    request.operation = 'queue_list'

    request.params.update(kwargs)

    resp = transport.send(request)

    if not resp.content:
        return {'links': [], 'queues': []}

    return resp.deserialized_content


def message_list(transport, request, queue_name, callback=None, **kwargs):
    """Gets a list of messages in queue `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: `six.text_type`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    :param kwargs: Optional arguments for this operation.
        - marker: Where to start getting messages from.
        - limit: Maximum number of messages to get.
        - echo: Whether to get our own messages.
        - include_claimed: Whether to include claimed
            messages.
    """

    request.operation = 'message_list'
    request.params['queue_name'] = queue_name

    # NOTE(flaper87): Assume passed params
    # are accepted by the API, if not, the
    # API itself will raise an error.
    request.params.update(kwargs)

    resp = transport.send(request)

    if not resp.content:
        # NOTE(flaper87): We could also return None
        # or an empty dict, however, we're giving
        # more value to a consistent API here by
        # returning a compliant dict with empty
        # `links` and `messages`
        return {'links': [], 'messages': []}

    return resp.deserialized_content


def message_post(transport, request, queue_name, messages, callback=None):
    """Post messages to `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: `six.text_type`
    :param messages: One or more messages to post.
    :param messages: `list`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_post'
    request.params['queue_name'] = queue_name
    request.content = json.dumps(messages)

    resp = transport.send(request)
    return resp.deserialized_content


def message_get(transport, request, queue_name, message_id, callback=None):
    """Gets one message from the queue by id

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: `six.text_type`
    :param message_id: Message reference.
    :param message_id: `six.text_type`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_get'
    request.params['queue_name'] = queue_name
    request.params['message_id'] = message_id

    resp = transport.send(request)
    return resp.deserialized_content


def message_get_many(transport, request, queue_name, messages, callback=None):
    """Gets many messages by id

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: `six.text_type`
    :param messages: Messages references.
    :param messages: list of `six.text_type`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_get_many'
    request.params['queue_name'] = queue_name
    request.params['ids'] = messages

    resp = transport.send(request)
    return resp.deserialized_content


def message_delete(transport, request, queue_name, message_id,
                   claim_id=None, callback=None):
    """Deletes messages from `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: `six.text_type`
    :param message_id: Message reference.
    :param message_id: `six.text_type`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_delete'
    request.params['queue_name'] = queue_name
    request.params['message_id'] = message_id
    if claim_id:
        request.params['claim_id'] = claim_id

    transport.send(request)


def claim_create(transport, request, queue_name, **kwargs):
    """Creates a Claim `claim_id` on the queue `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    """

    request.operation = 'claim_create'
    request.params['queue_name'] = queue_name
    request.content = json.dumps(kwargs)

    resp = transport.send(request)
    return resp.deserialized_content


def claim_get(transport, request, queue_name, claim_id):
    """Gets a Claim `claim_id`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    """

    request.operation = 'claim_get'
    request.params['queue_name'] = queue_name
    request.params['claim_id'] = claim_id

    resp = transport.send(request)
    return resp.deserialized_content


def claim_update(transport, request, queue_name, claim_id, **kwargs):
    """Updates a Claim `claim_id`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    """

    request.operation = 'claim_update'
    request.params['queue_name'] = queue_name
    request.params['claim_id'] = claim_id
    request.content = json.dumps(kwargs)

    resp = transport.send(request)
    return resp.deserialized_content


def claim_delete(transport, request, queue_name, claim_id):
    """Deletes a Claim `claim_id`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    """
    request.operation = 'claim_delete'
    request.params['queue_name'] = queue_name
    request.params['claim_id'] = claim_id

    transport.send(request)


def shard_create(transport, request, shard_name, shard_data):
    """Creates a shard called `shard_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param shard_name: Shard reference name.
    :type shard_name: `six.text_type`
    :param shard_data: Shard's properties, i.e: weight, uri, options.
    :type shard_data: `dict`
    """

    request.operation = 'shard_create'
    request.params['shard_name'] = shard_name
    request.content = json.dumps(shard_data)
    transport.send(request)


def shard_delete(transport, request, shard_name):
    """Deletes the shard `shard_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param shard_name: Shard reference name.
    :type shard_name: `six.text_type`
    """

    request.operation = 'shard_delete'
    request.params['shard_name'] = shard_name
    transport.send(request)


def health(transport, request, callback=None):
    """Check the health of web head for load balancing

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'health'
    resp = transport.send(request)
    return resp.deserialized_content
