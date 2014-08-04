# Copyright 2014 Red Hat, Inc.
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
import six

from cliff import command
from cliff import lister
from cliff import show

from openstackclient.common import utils


class CreateQueues(show.ShowOne):
    """List available queues."""

    log = logging.getLogger(__name__ + ".CreateQueues")

    def get_parser(self, prog_name):
        parser = super(CreateQueues, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.queuing

        name = parsed_args.name
        client.queue(name)

        return zip(*sorted(six.iteritems({"name": name})))


class DeleteQueues(command.Command):
    """List available queues."""

    log = logging.getLogger(__name__ + ".DeleteQueues")

    def get_parser(self, prog_name):
        parser = super(DeleteQueues, self).get_parser(prog_name)
        parser.add_argument(
            "name",
            metavar="<name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.queuing
        client.queue(parsed_args.name).delete()


class ListQueues(lister.Lister):
    """List available queues."""

    log = logging.getLogger(__name__ + ".ListQueues")

    def get_parser(self, prog_name):
        parser = super(ListQueues, self).get_parser(prog_name)
        parser.add_argument(
            "--marker",
            metavar="<queue_id>",
            help="Queue's paging marker")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            help="Page size limit")

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.queuing

        kwargs = {}
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit

        data = client.queues(**kwargs)
        columns = ["_Name"]

        return (columns, (utils.get_item_properties(s, columns) for s in data))
