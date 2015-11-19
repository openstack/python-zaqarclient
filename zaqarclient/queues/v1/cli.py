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

import json
import logging

from cliff import command
from cliff import lister
from cliff import show

from openstackclient.common import utils


class CreateQueue(show.ShowOne):
    """Create a queue"""

    log = logging.getLogger(__name__ + ".CreateQueue")

    def get_parser(self, prog_name):
        parser = super(CreateQueue, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name
        data = client.queue(queue_name)

        columns = ('Name',)
        return columns, utils.get_item_properties(data, columns)


class DeleteQueue(command.Command):
    """Delete a queue"""

    log = logging.getLogger(__name__ + ".DeleteQueue")

    def get_parser(self, prog_name):
        parser = super(DeleteQueue, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name

        client.queue(queue_name).delete()


class ListQueues(lister.Lister):
    """List available queues"""

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

        client = self.app.client_manager.messaging

        kwargs = {}
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit

        data = client.queues(**kwargs)
        columns = ("Name", )
        return (columns,
                (utils.get_item_properties(s, columns) for s in data))


class CheckQueueExistence(show.ShowOne):
    """Check queue existence"""

    log = logging.getLogger(__name__ + ".CheckQueueExistence")

    def get_parser(self, prog_name):
        parser = super(CheckQueueExistence, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        columns = ('Exists',)
        data = dict(exists=queue.exists())
        return columns, utils.get_dict_properties(data, columns)


class SetQueueMetadata(command.Command):
    """Set queue metadata"""

    log = logging.getLogger(__name__ + ".SetQueueMetadata")

    def get_parser(self, prog_name):
        parser = super(SetQueueMetadata, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        parser.add_argument(
            "queue_metadata",
            metavar="<queue_metadata>",
            help="Queue metadata")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name
        queue_metadata = parsed_args.queue_metadata
        queue_exists = client.queue(queue_name, auto_create=False).exists()

        if not queue_exists:
            raise RuntimeError("Queue(%s) does not exist." % queue_name)

        try:
            valid_metadata = json.loads(queue_metadata)
        except ValueError:
            raise RuntimeError("Queue metadata(%s) is not a valid json." %
                               queue_metadata)

        client.queue(queue_name, auto_create=False).\
            metadata(new_meta=valid_metadata)


class GetQueueMetadata(show.ShowOne):
    """Get queue metadata"""

    log = logging.getLogger(__name__ + ".GetQueueMetadata")

    def get_parser(self, prog_name):
        parser = super(GetQueueMetadata, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        if not queue.exists():
            raise RuntimeError("Queue(%s) does not exist." % queue_name)

        columns = ("Metadata",)
        data = dict(metadata=queue.metadata())
        return columns, utils.get_dict_properties(data, columns)


class GetQueueStats(show.ShowOne):
    """Get queue stats"""

    log = logging.getLogger(__name__ + ".GetQueueStats")

    def get_parser(self, prog_name):
        parser = super(GetQueueStats, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        if not queue.exists():
            raise RuntimeError('Queue(%s) does not exist.' % queue_name)

        columns = ("Stats",)
        data = dict(stats=queue.stats)
        return columns, utils.get_dict_properties(data, columns)


class CreatePool(show.ShowOne):
    """Create a pool"""

    log = logging.getLogger(__name__ + ".CreatePool")

    def get_parser(self, prog_name):
        parser = super(CreatePool, self).get_parser(prog_name)
        parser.add_argument(
            "pool_name",
            metavar="<pool_name>",
            help="Name of the pool")
        parser.add_argument(
            "pool_uri",
            metavar="<pool_uri>",
            help="Storage engine URI")
        parser.add_argument(
            "pool_weight",
            type=int,
            metavar="<pool_weight>",
            help="weight of the pool")
        parser.add_argument(
            "--pool_group",
            metavar="<pool_group>",
            help="Group of the pool")
        parser.add_argument(
            "--pool_options",
            type=json.loads,
            default={},
            metavar="<pool_options>",
            help="An optional request component "
                 "related to storage-specific options")

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        kw_arg = {
            'uri': parsed_args.pool_uri,
            'weight': parsed_args.pool_weight,
            'options': parsed_args.pool_options
        }

        if parsed_args.pool_group:
            kw_arg.update({'group': parsed_args.pool_group})

        data = client.pool(parsed_args.pool_name, **kw_arg)

        if not data:
            raise RuntimeError('Failed to create pool(%s).' %
                               parsed_args.pool_name)

        columns = ('Name', 'Weight', 'URI', 'Group', 'Options')
        return columns, utils.get_item_properties(data, columns)


class ShowPool(show.ShowOne):
    """Display pool details"""

    log = logging.getLogger(__name__ + ".ShowPool")

    def get_parser(self, prog_name):
        parser = super(ShowPool, self).get_parser(prog_name)
        parser.add_argument(
            "pool_name",
            metavar="<pool_name>",
            help="Pool to display (name)",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.messaging
        pool_data = client.pool(parsed_args.pool_name,
                                auto_create=False).get()
        columns = ('Name', 'Weight', 'URI', 'Group', 'Options')
        return columns, utils.get_dict_properties(pool_data, columns)


class UpdatePool(show.ShowOne):
    """Update a pool attribute"""

    log = logging.getLogger(__name__+".UpdatePool")

    def get_parser(self, prog_name):
        parser = super(UpdatePool, self).get_parser(prog_name)
        parser.add_argument(
            "pool_name",
            metavar="<pool_name>",
            help="Name of the pool")
        parser.add_argument(
            "--pool_uri",
            metavar="<pool_uri>",
            help="Storage engine URI")
        parser.add_argument(
            "--pool_weight",
            type=int,
            metavar="<pool_weight>",
            help="Weight of the pool")
        parser.add_argument(
            "--pool_group",
            metavar="<pool_group>",
            help="Group of the pool")
        parser.add_argument(
            "--pool_options",
            type=json.loads,
            metavar="<pool_options>",
            help="An optional request component "
                 "related to storage-specific options")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging
        kw_arg = {}

        if parsed_args.pool_uri:
            kw_arg["uri"] = parsed_args.pool_uri
        if parsed_args.pool_weight:
            kw_arg["weight"] = parsed_args.pool_weight
        if parsed_args.pool_group:
            kw_arg["group"] = parsed_args.pool_group
        if parsed_args.pool_options:
            kw_arg["options"] = parsed_args.pool_options

        pool_obj = client.pool(parsed_args.pool_name, auto_create=False)
        pool_obj.update(kw_arg)
        pool_data = pool_obj.get()
        columns = ('Name', 'Weight', 'URI', 'Group', 'Options')
        return columns, utils.get_dict_properties(pool_data, columns)


class DeleteFlavor(command.Command):
    """Delete a flavor"""

    log = logging.getLogger(__name__ + ".DeleteFlavor")

    def get_parser(self, prog_name):
        parser = super(DeleteFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "flavor_name",
            metavar="<flavor_name>",
            help="Name of the flavor")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        flavor_name = parsed_args.flavor_name

        client.flavor(flavor_name).delete()
