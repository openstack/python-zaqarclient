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

from oslo.config import cfg

from marconiclient.queues.v1 import queues
from marconiclient import transport


_CLIENT_OPTIONS = [
    cfg.StrOpt('os_queues_url',
               help='Queues remote URL'),
]


class Client(object):

    def __init__(self, conf, url=None, version=1):
        self.conf = conf

        # NOTE(flaper87): This won't actually register
        # the CLI options until the class is instantiated
        # which is dumb. It'll refactored when the CLI API
        # work starts.
        self.conf.register_cli_opts(_CLIENT_OPTIONS)
        self.api_url = self.conf.os_queues_url or url
        self.api_version = version

    def transport(self):
        """Gets a transport based on conf."""
        return transport.get_transport_for_conf(self.conf)

    def queue(self, ref, **kwargs):
        """Returns a queue instance

        :param ref: Queue's reference id.
        :type ref: `six.text_type`

        :returns: A queue instance
        :rtype: `queues.Queue`
        """
        return queues.Queue(self, ref, **kwargs)
