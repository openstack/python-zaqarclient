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
