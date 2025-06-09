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
This module defines a lower level API for queues' v2. This level of the
API is responsible for packing up the final request, sending it to the server
and handling asynchronous requests.

Functions present in this module assume that:

    1. The transport instance is ready to `send` the
    request to the server.

    2. Transport instance holds the conf instance to use for this
    request.
"""

import datetime
import json

from oslo_utils import timeutils

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
    :type name: str
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """
    request.operation = operation
    request.params['queue_name'] = name
    resp = transport.send(request)
    return resp.deserialized_content


def queue_create(transport, request, name,
                 metadata=None, callback=None):
    """Creates a queue

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: str
    :param metadata: Queue's metadata object.
    :type metadata: `dict`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'queue_create'
    request.params['queue_name'] = name
    request.content = metadata and json.dumps(metadata)

    resp = transport.send(request)
    return resp.deserialized_content


def queue_update(transport, request, name, metadata, callback=None):
    """Updates a queue's metadata using PATCH

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: str
    :param metadata: Queue's metadata object.
    :type metadata: `list`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'queue_update'
    request.params['queue_name'] = name
    request.content = json.dumps(metadata)

    resp = transport.send(request)
    return resp.deserialized_content


def queue_exists(transport, request, name, callback=None):
    """Checks if the queue exists."""
    try:
        _common_queue_ops('queue_exists', transport,
                          request, name, callback=callback)
        return True
    except errors.ResourceNotFound:
        return False


def queue_get(transport, request, name, callback=None):
    """Retrieve a queue."""
    return _common_queue_ops('queue_get', transport,
                             request, name, callback=callback)


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


def queue_purge(transport, request, name, resource_types=None):
    """Purge resources under a queue

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: str
    :param resource_types: Resource types will be purged
    :type resource_types: `list`
    """
    request.operation = 'queue_purge'
    request.params['queue_name'] = name
    if resource_types:
        request.content = json.dumps({'resource_types': resource_types})

    resp = transport.send(request)
    return resp.deserialized_content


def message_list(transport, request, queue_name, callback=None, **kwargs):
    """Gets a list of messages in queue `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
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
    :type queue_name: str
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
    :type queue_name: str
    :param message_id: Message reference.
    :param message_id: str
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
    :type queue_name: str
    :param messages: Messages references.
    :param messages: list of str
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
    :type queue_name: str
    :param message_id: Message reference.
    :param message_id: str
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


def message_delete_many(transport, request, queue_name,
                        ids, callback=None):
    """Deletes `ids` messages from `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param ids: Ids of the messages to delete
    :type ids: List of str
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_delete_many'
    request.params['queue_name'] = queue_name
    request.params['ids'] = ids
    transport.send(request)


def message_pop(transport, request, queue_name,
                count, callback=None):
    """Pops out `count` messages from `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param count: Number of messages to pop.
    :type count: int
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'message_delete_many'
    request.params['queue_name'] = queue_name
    request.params['pop'] = count

    resp = transport.send(request)
    return resp.deserialized_content


def claim_create(transport, request, queue_name, **kwargs):
    """Creates a Claim `claim_id` on the queue `queue_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    """

    request.operation = 'claim_create'
    request.params['queue_name'] = queue_name

    if 'limit' in kwargs:
        request.params['limit'] = kwargs.pop('limit')

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


def pool_get(transport, request, pool_name, callback=None):
    """Gets pool data

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param pool_name: Pool reference name.
    :type pool_name: str

    """

    request.operation = 'pool_get'
    request.params['pool_name'] = pool_name

    resp = transport.send(request)
    return resp.deserialized_content


def pool_create(transport, request, pool_name, pool_data):
    """Creates a pool called `pool_name`


    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param pool_name: Pool reference name.
    :type pool_name: str
    :param pool_data: Pool's properties, i.e: weight, uri, options.
    :type pool_data: `dict`
    """

    request.operation = 'pool_create'
    request.params['pool_name'] = pool_name
    request.content = json.dumps(pool_data)
    transport.send(request)


def pool_update(transport, request, pool_name, pool_data):
    """Updates the pool `pool_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param pool_name: Pool reference name.
    :type pool_name: str
    :param pool_data: Pool's properties, i.e: weight, uri, options.
    :type pool_data: `dict`
    """

    request.operation = 'pool_update'
    request.params['pool_name'] = pool_name
    request.content = json.dumps(pool_data)

    resp = transport.send(request)
    return resp.deserialized_content


def pool_list(transport, request, **kwargs):
    """Gets a list of pools

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param kwargs: Optional arguments for this operation.
        - marker: Where to start getting pools from.
        - limit: Maximum number of pools to get.
    """

    request.operation = 'pool_list'
    request.params.update(kwargs)

    resp = transport.send(request)

    if not resp.content:
        return {'links': [], 'pools': []}

    return resp.deserialized_content


def pool_delete(transport, request, pool_name):
    """Deletes the pool `pool_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param pool_name: Pool reference name.
    :type pool_name: str
    """

    request.operation = 'pool_delete'
    request.params['pool_name'] = pool_name
    transport.send(request)


def flavor_create(transport, request, name, flavor_data):
    """Creates a flavor called `name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Flavor reference name.
    :type name: str
    :param flavor_data: Flavor's properties, i.e: pool, capabilities.
    :type flavor_data: `dict`
    """

    request.operation = 'flavor_create'
    request.params['flavor_name'] = name
    request.content = json.dumps(flavor_data)
    transport.send(request)


def flavor_get(transport, request, flavor_name, callback=None):
    """Gets flavor data

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param flavor_name: Flavor reference name.
    :type flavor_name: str

    """

    request.operation = 'flavor_get'
    request.params['flavor_name'] = flavor_name

    resp = transport.send(request)
    return resp.deserialized_content


def flavor_update(transport, request, flavor_name, flavor_data):
    """Updates the flavor `flavor_name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param flavor_name: Flavor reference name.
    :type flavor_name: str
    :param flavor_data: Flavor's properties, i.e: pool, capabilities.
    :type flavor_data: `dict`
    """

    request.operation = 'flavor_update'
    request.params['flavor_name'] = flavor_name
    request.content = json.dumps(flavor_data)

    resp = transport.send(request)
    return resp.deserialized_content


def flavor_list(transport, request, **kwargs):
    """Gets a list of flavors

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param kwargs: Optional arguments for this operation.
        - marker: Where to start getting flavors from.
        - limit: Maximum number of flavors to get.
    """

    request.operation = 'flavor_list'
    request.params.update(kwargs)

    resp = transport.send(request)

    if not resp.content:
        return {'links': [], 'flavors': []}

    return resp.deserialized_content


def flavor_delete(transport, request, name):
    """Deletes the flavor `name`

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Flavor reference name.
    :type name: str
    """

    request.operation = 'flavor_delete'
    request.params['flavor_name'] = name
    transport.send(request)


def signed_url_create(transport, request, queue_name, paths=None,
                      ttl_seconds=None, project_id=None, methods=None):
    """Creates a signed URL given a queue name

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: name of Queue for the URL to access
    :type name: str
    :param paths: Allowed actions. Options: messages, subscriptions, claims
    :type name: list
    :param ttl_seconds: Seconds the URL will be valid for, default 86400
    :type name: int
    :param project_id: defaults to None
    :type name: str
    :param methods: HTTP methods to allow, defaults to ["GET"]
    :type name: `list`
    """

    request.operation = 'signed_url_create'
    request.params['queue_name'] = queue_name

    body = {}
    if ttl_seconds is not None:
        expiry = (timeutils.utcnow() + datetime.timedelta(seconds=ttl_seconds))
        body['expires'] = expiry.isoformat()

    if project_id is not None:
        body['project_id'] = project_id

    if paths is not None:
        body['paths'] = paths

    if methods is not None:
        body['methods'] = methods

    request.content = json.dumps(body)

    resp = transport.send(request)
    return resp.deserialized_content


def subscription_create(transport, request, queue_name, subscription_data):
    """Creates a new subscription against the `queue_name`


    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param subscription_data: Subscription's properties, i.e: subscriber,
        ttl, options.
    :type subscription_data: `dict`
    """

    request.operation = 'subscription_create'
    request.params['queue_name'] = queue_name
    request.content = json.dumps(subscription_data)
    resp = transport.send(request)

    return resp.deserialized_content


def subscription_get(transport, request, queue_name, subscription_id):
    """Gets a particular subscription data

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param subscription_id: ID of subscription.
    :type subscription_id: str

    """

    request.operation = 'subscription_get'
    request.params['queue_name'] = queue_name
    request.params['subscription_id'] = subscription_id

    resp = transport.send(request)
    return resp.deserialized_content


def subscription_update(transport, request, queue_name, subscription_id,
                        subscription_data):
    """Updates the subscription

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param subscription_id: ID of subscription.
    :type subscription_id: str
    :param subscription_data: Subscription's properties, i.e: subscriber,
        ttl, options.
    :type subscription_data: `dict`
    """

    request.operation = 'subscription_update'
    request.params['queue_name'] = queue_name
    request.params['subscription_id'] = subscription_id
    request.content = json.dumps(subscription_data)

    resp = transport.send(request)
    return resp.deserialized_content


def subscription_delete(transport, request, queue_name, subscription_id):
    """Deletes the subscription

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param subscription_id: ID of subscription.
    :type subscription_id: str
    """

    request.operation = 'subscription_delete'
    request.params['queue_name'] = queue_name
    request.params['subscription_id'] = subscription_id
    transport.send(request)


def subscription_list(transport, request, queue_name, **kwargs):
    """Gets a list of subscriptions

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: Queue reference name.
    :type queue_name: str
    :param kwargs: Optional arguments for this operation.
        - marker: Where to start getting subscriptions from.
        - limit: Maximum number of subscriptions to get.
    """

    request.operation = 'subscription_list'
    request.params['queue_name'] = queue_name
    request.params.update(kwargs)

    resp = transport.send(request)

    if not resp.content:
        return {'links': [], 'subscriptions': []}

    return resp.deserialized_content


def ping(transport, request, callback=None):
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

    request.operation = 'ping'
    try:
        transport.send(request)
        return True
    except Exception:
        return False


def health(transport, request, callback=None):
    """Get detailed health status of Zaqar server

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


def homedoc(transport, request, callback=None):
    """Get the detailed resource doc of Zaqar server

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param callback: Optional callable to use as callback.
        If specified, this request will be sent asynchronously.
        (IGNORED UNTIL ASYNC SUPPORT IS COMPLETE)
    :type callback: Callable object.
    """

    request.operation = 'homedoc'
    resp = transport.send(request)
    return resp.deserialized_content
