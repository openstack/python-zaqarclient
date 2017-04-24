# Copyright (c) 2015 Red Hat, Inc.
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

from zaqarclient.queues.v1 import api


class V2(api.V1_1):
    label = 'v2'
    schema = api.V1_1.schema.copy()


V2.schema.update({
    'queue_purge': {
        'ref': 'queues/{queue_name}/purge',
        'method': 'POST',
        'required': ['queue_name'],
        'properties': {
            'queue_name': {'type': 'string'}
        }
    },
    'signed_url_create': {
        'ref': 'queues/{queue_name}/share',
        'method': 'POST',
        'required': ['queue_name'],
        'properties': {
            'queue_name': {'type': 'string'}
        },
    },
    'subscription_create': {
        'ref': 'queues/{queue_name}/subscriptions',
        'method': 'POST',
        'required': ['queue_name'],
        'properties': {
            'queue_name': {'type': 'string'}
        },
    },
    'subscription_get': {
        'ref': 'queues/{queue_name}/subscriptions/{subscription_id}',
        'method': 'GET',
        'required': ['queue_name', 'subscription_id'],
        'properties': {
            'queue_name': {'type': 'string'},
            'subscription_id': {'type': 'string'}
        },
    },
    'subscription_update': {
        'ref': 'queues/{queue_name}/subscriptions/{subscription_id}',
        'method': 'PATCH',
        'required': ['queue_name', 'subscription_id'],
        'properties': {
            'queue_name': {'type': 'string'},
            'subscription_id': {'type': 'string'}
        }
    },
    'subscription_delete': {
        'ref': 'queues/{queue_name}/subscriptions/{subscription_id}',
        'method': 'DELETE',
        'required': ['queue_name', 'subscription_id'],
        'properties': {
            'queue_name': {'type': 'string'},
            'subscription_id': {'type': 'string'}
        }
    },
    'subscription_list': {
        'ref': 'queues/{queue_name}/subscriptions',
        'method': 'GET',
        'properties': {
            'marker': {'type': 'string'},
            'limit': {'type': 'integer'},
            'detailed': {'type': 'boolean'}
        }
    },

    'ping': {
        'ref': 'ping',
        'method': 'GET',
    },

    'health': {
        'ref': 'health',
        'method': 'GET',
    },

    'homedoc': {
        'ref': '',
        'method': 'GET',
    },
})
