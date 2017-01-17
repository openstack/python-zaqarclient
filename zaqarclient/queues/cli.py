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

"""OpenStackClient plugin for Messaging service."""

from osc_lib import utils
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

DEFAULT_QUEUES_API_VERSION = '2'
API_VERSION_OPTION = 'os_queues_api_version'
API_NAME = "messaging"
API_VERSIONS = {
    "1": "zaqarclient.queues.v1.client.Client",
    "1.1": "zaqarclient.queues.v1.client.Client",
    "2": "zaqarclient.queues.v2.client.Client",
}

_MESSAGING_ENDPOINT = None


def make_client(instance):
    """Returns an queues service client."""
    global _MESSAGING_ENDPOINT
    version = instance._api_version[API_NAME]
    try:
        version = int(version)
    except ValueError:
        version = float(version)

    queues_client = utils.get_client_class(
        API_NAME,
        version,
        API_VERSIONS)

    # TODO(wangxiyuan): Use public attributes instead of private attributes.
    if not _MESSAGING_ENDPOINT:
        _MESSAGING_ENDPOINT = instance.get_endpoint_for_service_type(
            API_NAME,
            region_name=instance._region_name,
            interface=instance._interface
        )

    auth_params = instance.get_configuration()['auth']
    auth_params.update({
        "auth_token": instance.auth.get_token(instance.session),
        "insecure": instance._insecure,
        "cacert": instance._cacert,
        "region_name": instance._region_name
    })

    conf = {
        "auth_opts": {'options': auth_params}
    }

    LOG.debug('Instantiating queues service client: %s', queues_client)
    return queues_client(
        _MESSAGING_ENDPOINT,
        version,
        conf
    )


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
