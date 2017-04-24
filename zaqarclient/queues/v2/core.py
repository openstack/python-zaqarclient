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

from zaqarclient.queues.v1 import core

queue_create = core.queue_create
queue_exists = core.queue_exists
queue_get = core.queue_get
queue_get_metadata = core.queue_get_metadata
queue_set_metadata = core.queue_set_metadata
queue_get_stats = core.queue_get_stats
queue_delete = core.queue_delete
queue_list = core.queue_list
message_get = core.message_get
message_list = core.message_list
message_post = core.message_post
message_delete = core.message_delete
message_delete_many = core.message_delete_many
pool_get = core.pool_get
pool_create = core.pool_create
pool_delete = core.pool_delete
pool_update = core.pool_update
pool_list = core.pool_list
flavor_get = core.flavor_get
flavor_create = core.flavor_create
flavor_delete = core.flavor_delete
flavor_update = core.flavor_update
flavor_list = core.flavor_list
claim_create = core.claim_create
claim_get = core.claim_get
claim_update = core.claim_update
claim_delete = core.claim_delete


def queue_update(transport, request, name, metadata, callback=None):
    """Updates a queue's metadata using PATCH for API v2

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: `six.text_type`
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


def queue_purge(transport, request, name, resource_types=None):
    """Purge resources under a queue

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param name: Queue reference name.
    :type name: `six.text_type`
    :param resource_types: Resource types will be purged
    :type resource_types: `list`
    """
    request.operation = 'queue_purge'
    request.params['queue_name'] = name
    if resource_types:
        request.content = json.dumps({'resource_types': resource_types})

    resp = transport.send(request)
    return resp.deserialized_content


def signed_url_create(transport, request, queue_name, paths=None,
                      ttl_seconds=None, project_id=None, methods=None):
    """Creates a signed URL given a queue name

    :param transport: Transport instance to use
    :type transport: `transport.base.Transport`
    :param request: Request instance ready to be sent.
    :type request: `transport.request.Request`
    :param queue_name: name of Queue for the URL to access
    :type name: `six.text_type`
    :param paths: Allowed actions. Options: messages, subscriptions, claims
    :type name: list
    :param ttl_seconds: Seconds the URL will be valid for, default 86400
    :type name: int
    :param project_id: defaults to None
    :type name: `six.text_type`
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
    :type queue_name: `six.text_type`
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
    :type queue_name: `six.text_type`
    :param subscription_id: ID of subscription.
    :type subscription_id: `six.text_type`

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
    :type queue_name: `six.text_type`
    :param subscription_id: ID of subscription.
    :type subscription_id: `six.text_type`
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
    :type queue_name: `six.text_type`
    :param subscription_id: ID of subscription.
    :type subscription_id: `six.text_type`
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
    :type queue_name: `six.text_type`
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
