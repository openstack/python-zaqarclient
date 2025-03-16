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

from zaqarclient.transport import api


class V2(api.Api):
    label = 'v2'
    schema = {
        'queue_list': {
            'ref': 'queues',
            'method': 'GET',
            'properties': {
                'marker': {'type': 'string'},
                'limit': {'type': 'integer'},
                'detailed': {'type': 'boolean'}
            }
        },
        'queue_create': {
            'ref': 'queues/{queue_name}',
            'method': 'PUT',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            },
        },
        'queue_get': {
            'ref': 'queues/{queue_name}',
            'method': 'GET',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },
        'queue_exists': {
            'ref': 'queues/{queue_name}',
            'method': 'HEAD',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },
        'queue_update': {
            'ref': 'queues/{queue_name}',
            'method': 'PATCH',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },
        'queue_delete': {
            'ref': 'queues/{queue_name}',
            'method': 'DELETE',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },
        'queue_get_stats': {
            'ref': 'queues/{queue_name}/stats',
            'method': 'GET',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },
        'queue_purge': {
            'ref': 'queues/{queue_name}/purge',
            'method': 'POST',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'}
            }
        },

        'message_list': {
            'ref': 'queues/{queue_name}/messages',
            'method': 'GET',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'},
                'marker': {'type': 'string'},
                'limit': {'type': 'integer'},
                'echo': {'type': 'boolean'},
                'include_claimed': {'type': 'boolean'},
            }
        },
        'message_post': {
            'ref': 'queues/{queue_name}/messages',
            'method': 'POST',
            'required': ['queue_name', 'message_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'claim_id': {'type': 'string'},
            }
        },
        'message_get': {
            'ref': 'queues/{queue_name}/messages/{message_id}',
            'method': 'GET',
            'required': ['queue_name', 'message_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'message_id': {'type': 'string'},
                'claim_id': {'type': 'string'},
            }
        },
        'message_get_many': {
            'ref': 'queues/{queue_name}/messages',
            'method': 'GET',
            'required': ['queue_name', 'ids'],
            'properties': {
                'queue_name': {'type': 'string'},
                'ids': {'type': 'string'},
                'claim_id': {'type': 'string'},
            }
        },
        'message_delete': {
            'ref': 'queues/{queue_name}/messages/{message_id}',
            'method': 'DELETE',
            'required': ['queue_name', 'message_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'message_id': {'type': 'string'},
                'claim_id': {'type': 'string'},
            }
        },
        'message_delete_many': {
            'ref': 'queues/{queue_name}/messages',
            'method': 'DELETE',
            'required': ['queue_name', 'ids'],
            'properties': {
                'queue_name': {'type': 'string'},
                'ids': {'type': 'string'},
            }
        },
        'message_pop': {
            'ref': 'queues/{queue_name}/messages',
            'method': 'DELETE',
            'required': ['queue_name', 'pop'],
            'properties': {
                'queue_name': {'type': 'string'},
                'pop': {'type': 'integer'},
            }
        },

        'pool_list': {
            'ref': 'pools',
            'method': 'GET',
            'properties': {
                'pool_name': {'type': 'string'},
                'marker': {'type': 'string'},
                'limit': {'type': 'integer'},
                'detailed': {'type': 'boolean'}
            }
        },
        'pool_create': {
            'ref': 'pools/{pool_name}',
            'method': 'PUT',
            'required': ['pool_name'],
            'properties': {
                'pool_name': {'type': 'string'},
            }
        },
        'pool_get': {
            'ref': 'pools/{pool_name}',
            'method': 'GET',
            'required': ['pool_name'],
            'properties': {
                'pool_name': {'type': 'string'},
            }
        },
        'pool_update': {
            'ref': 'pools/{pool_name}',
            'method': 'PATCH',
            'required': ['pool_name'],
            'properties': {
                'pool_name': {'type': 'string'}
            }
        },
        'pool_delete': {
            'ref': 'pools/{pool_name}',
            'method': 'DELETE',
            'required': ['pool_name'],
            'properties': {
                'pool_name': {'type': 'string'},
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

        'flavor_list': {
            'ref': 'flavors',
            'method': 'GET',
            'properties': {
                'flavor_name': {'type': 'string'},
                'marker': {'type': 'string'},
                'limit': {'type': 'integer'},
                'detailed': {'type': 'boolean'}
            }
        },
        'flavor_create': {
            'ref': 'flavors/{flavor_name}',
            'method': 'PUT',
            'required': ['flavor_name'],
            'properties': {
                'flavor_name': {'type': 'string'},
            }
        },
        'flavor_get': {
            'ref': 'flavors/{flavor_name}',
            'method': 'GET',
            'required': ['flavor_name'],
            'properties': {
                'flavor_name': {'type': 'string'},
            }
        },
        'flavor_update': {
            'ref': 'flavors/{flavor_name}',
            'method': 'PATCH',
            'required': ['flavor_name'],
            'properties': {
                'flavor_name': {'type': 'string'}
            }
        },
        'flavor_delete': {
            'ref': 'flavors/{flavor_name}',
            'method': 'DELETE',
            'required': ['flavor_name'],
            'properties': {
                'flavor_name': {'type': 'string'},
            }
        },

        'claim_create': {
            'ref': 'queues/{queue_name}/claims',
            'method': 'POST',
            'required': ['queue_name'],
            'properties': {
                'queue_name': {'type': 'string'},
                'limit': {'type': 'integer'},
                'grace': {'type': 'integer'}
            }
        },
        'claim_get': {
            'ref': 'queues/{queue_name}/claims/{claim_id}',
            'method': 'GET',
            'required': ['queue_name', 'claim_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'claim_id': {'type': 'string'}
            }
        },
        'claim_update': {
            'ref': 'queues/{queue_name}/claims/{claim_id}',
            'method': 'PATCH',
            'required': ['queue_name', 'claim_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'claim_id': {'type': 'string'}
            }
        },
        'claim_delete': {
            'ref': 'queues/{queue_name}/claims/{claim_id}',
            'method': 'DELETE',
            'required': ['queue_name', 'claim_id'],
            'properties': {
                'queue_name': {'type': 'string'},
                'claim_id': {'type': 'string'}
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
    }
