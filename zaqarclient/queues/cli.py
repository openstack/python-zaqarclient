# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from openstackclient.common import utils


LOG = logging.getLogger(__name__)

DEFAULT_QUEUES_API_VERSION = '1'
API_VERSION_OPTION = 'os_queues_api_version'
API_NAME = "queuing"
API_VERSIONS = {
    "1": "zaqarclient.queues.v1.client.Client",
}


def make_client(instance):
    """Returns an queues service client."""
    queues_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    if not instance._url:
        instance._url = instance.get_endpoint_for_service_type(API_NAME)

    return queues_client(url=instance._url)


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-queues-api-version',
        metavar='<queues-api-version>',
        default=utils.env(
            'OS_QUEUES_API_VERSION',
            default=DEFAULT_QUEUES_API_VERSION),
        help=('Queues API version, default=' +
              DEFAULT_QUEUES_API_VERSION +
              ' (Env: OS_QUEUES_API_VERSION)'))
    return parser
