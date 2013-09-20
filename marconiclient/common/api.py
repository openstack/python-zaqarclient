# Copyright (c) 2013 Rackspace, Inc.
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

import collections


ApiInfo = collections.namedtuple('ApiInfo', 'mandatory optional')

_API_DATA = dict(
    create_queue=ApiInfo(
        mandatory=set(['queue_name']), optional=set()),
    list_queues=ApiInfo(
        mandatory=set(), optional=set(['marker', 'limit', 'detailed'])),
    queue_exists=ApiInfo(mandatory=set(['queue_name']), optional=set()),
    delete_queue=ApiInfo(mandatory=set(['queue_name']), optional=set()),
    set_queue_metadata=ApiInfo(
        mandatory=set(['queue_name', 'metadata']), optional=set()),
    get_queue_metadata=ApiInfo(
        mandatory=set(['queue_name']), optional=set()),
    get_queue_stats=ApiInfo(mandatory=set(['queue_name']), optional=set()),
    list_messages=ApiInfo(
        mandatory=set(['queue_name']),
        optional=set(['marker', 'limit', 'echo', 'include_claimed'])),
    get_message=ApiInfo(
        mandatory=set(['queue_name', 'message_id']),
        optional=set(['claim_id'])),
    get_messages_by_id=ApiInfo(
        mandatory=set(['queue_name', 'message_ids']),
        optional=set()),
    post_messages=ApiInfo(
        mandatory=set(['queue_name', 'messagedata']), optional=set()),
    delete_message=ApiInfo(
        mandatory=set(['queue_name', 'message_id']),
        optional=set(['claim_id'])),
    delete_messages_by_id=ApiInfo(
        mandatory=set(['queue_name', 'message_ids']), optional=set()),
    claim_messages=ApiInfo(
        mandatory=set(['queue_name', 'ttl', 'grace_period']),
        optional=set(['limit'])),
    query_claim=ApiInfo(
        mandatory=set(['queue_name', 'claim_id']), optional=set()),
    update_claim=ApiInfo(
        mandatory=set(['queue_name', 'claim_id', 'ttl']), optional=set()),
    release_claim=ApiInfo(
        mandatory=set(['queue_name', 'claim_id']), optional=set()),
)


def info():
    """A dict where the keys and values are valid operations and `ApiInfo`
    named tuples respectively.
    The `ApiInfo` named tuples have a `mandatory` and an `optional` property
    that list the params for the respective operation.
    """
    return _API_DATA.copy()
