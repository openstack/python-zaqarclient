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

from marconiclient.transport import api


class V1(api.Api):

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

        'queue_exists': {
            'ref': 'queues/{queue_name}',
            'method': 'HEAD',
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

        'queue_set_metadata': {
            'ref': 'queues/{queue_name}/metadata',
            'method': 'PUT',
            'required': ['queue_name'],
            'properties': {
                # NOTE(flaper87): Metadata is part
                # of the request content. No need to
                # add it here.
                'queue_name': {'type': 'string'},
            }
        },

        'queue_get_metadata': {
            'ref': 'queues/{queue_name}/metadata',
            'method': 'GET',
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
    }
