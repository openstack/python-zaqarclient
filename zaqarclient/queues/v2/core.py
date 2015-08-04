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
