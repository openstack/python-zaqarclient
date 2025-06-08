# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os

from osc_lib.command import command
from osc_lib import utils
from oslo_log import log as logging

from zaqarclient._i18n import _
from zaqarclient.transport import errors


def _get_client(obj, parsed_args):
    obj.log.debug("take_action(%s)" % parsed_args)
    return obj.app.client_manager.messaging


class CreateQueue(command.ShowOne):
    """Create a queue"""

    _description = _("Create a queue")
    log = logging.getLogger(__name__ + ".CreateQueue")

    def get_parser(self, prog_name):
        parser = super(CreateQueue, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        data = client.queue(queue_name, force_create=True)
        columns = ('Name',)
        return columns, utils.get_item_properties(data, columns)


class DeleteQueue(command.Command):
    """Delete a queue"""

    _description = _("Delete a queue")
    log = logging.getLogger(__name__ + ".DeleteQueue")

    def get_parser(self, prog_name):
        parser = super(DeleteQueue, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        client.queue(queue_name).delete()


class ListQueues(command.Lister):
    """List available queues"""

    _description = _("List available queues")
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
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="If show detailed information of queue")
        parser.add_argument(
            "--with_count",
            action="store_true",
            help="If show amount information of queue")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        kwargs = {}
        columns = ["Name"]
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit
        if parsed_args.detailed is not None and parsed_args.detailed:
            kwargs["detailed"] = parsed_args.detailed
            columns.extend(["Metadata_Dict", "Href"])
        if parsed_args.with_count is not None and parsed_args.with_count:
            kwargs["with_count"] = parsed_args.with_count

        data, count = client.queues(**kwargs)
        if count:
            print("Queues in total: %s" % count)
        columns = tuple(columns)
        return (columns, (utils.get_item_properties(s, columns) for s in data))


class GetQueueStats(command.ShowOne):
    """Get queue stats"""

    _description = _("Get queue stats")
    log = logging.getLogger(__name__ + ".GetQueueStats")

    def get_parser(self, prog_name):
        parser = super(GetQueueStats, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        try:
            stats = queue.stats
        except errors.ResourceNotFound:
            raise RuntimeError('Queue(%s) does not exist.' % queue_name)

        columns = ("Stats",)
        data = dict(stats=stats)
        return columns, utils.get_dict_properties(data, columns)


class SetQueueMetadata(command.Command):
    """Set queue metadata"""

    _description = _("Set queue metadata")
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
            help="Queue metadata, All the metadata of "
                 "the queue will be replaced by queue_metadata")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        queue_metadata = parsed_args.queue_metadata

        try:
            valid_metadata = json.loads(queue_metadata)
        except ValueError:
            raise RuntimeError("Queue metadata(%s) is not a valid json." %
                               queue_metadata)

        client.queue(queue_name, auto_create=False).\
            metadata(new_meta=valid_metadata)


class GetQueueMetadata(command.ShowOne):
    """Get queue metadata"""

    _description = _("Get queue metadata")
    log = logging.getLogger(__name__ + ".GetQueueMetadata")

    def get_parser(self, prog_name):
        parser = super(GetQueueMetadata, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        columns = ("Metadata",)
        data = dict(metadata=queue.metadata())
        return columns, utils.get_dict_properties(data, columns)


class PostMessages(command.Command):
    """Post messages for a given queue"""

    _description = _("Post messages for a given queue")
    log = logging.getLogger(__name__ + ".PostMessages")

    def get_parser(self, prog_name):
        parser = super(PostMessages, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        parser.add_argument(
            "messages",
            type=json.loads,
            metavar="<messages>",
            help="Messages to be posted.")
        parser.add_argument(
            "--client-id",
            metavar="<client_id>",
            default=os.environ.get("OS_MESSAGE_CLIENT_ID"),
            help="A UUID for each client instance.")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        if not parsed_args.client_id:
            raise AttributeError("<--client-id> option is missing and "
                                 "environment variable OS_MESSAGE_CLIENT_ID "
                                 "is not set. Please at least either pass in "
                                 "the client id or set the environment "
                                 "variable")
        else:
            client.client_uuid = parsed_args.client_id

        queue = client.queue(parsed_args.queue_name)
        queue.post(parsed_args.messages)


class ListMessages(command.Lister):
    """List all messages for a given queue"""

    _description = _("List all messages for a given queue")
    log = logging.getLogger(__name__ + ".ListMessages")

    def get_parser(self, prog_name):
        parser = super(ListMessages, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        parser.add_argument(
            "--message-ids",
            metavar="<message_ids>",
            help="List of messages' ids to retrieve")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            help="Maximum number of messages to get")
        parser.add_argument(
            "--echo",
            action="store_true",
            help="Whether to get this client's own messages")
        parser.add_argument(
            "--include-claimed",
            action="store_true",
            help="Whether to include claimed messages")
        parser.add_argument(
            "--include-delayed",
            action="store_true",
            help="Whether to include delayed messages")
        parser.add_argument(
            "--client-id",
            metavar="<client_id>",
            default=os.environ.get("OS_MESSAGE_CLIENT_ID"),
            help="A UUID for each client instance.")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        if not parsed_args.client_id:
            raise AttributeError("<--client-id> option is missing and "
                                 "environment variable OS_MESSAGE_CLIENT_ID "
                                 "is not set. Please at least either pass in "
                                 "the client id or set the environment "
                                 "variable")
        else:
            client.client_uuid = parsed_args.client_id

        kwargs = {}
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit
        if parsed_args.echo is not None:
            kwargs["echo"] = parsed_args.echo
        if parsed_args.include_claimed is not None:
            kwargs["include_claimed"] = parsed_args.include_claimed
        if parsed_args.include_delayed is not None:
            kwargs["include_delayed"] = parsed_args.include_delayed

        queue = client.queue(parsed_args.queue_name)

        if parsed_args.message_ids:
            messages = queue.messages(parsed_args.message_ids.split(','),
                                      **kwargs)
        else:
            messages = queue.messages(**kwargs)

        columns = ("ID", "Body", "TTL", "Age", "Claim ID", "Checksum")
        return (columns,
                (utils.get_item_properties(s, columns) for s in messages))


class PurgeQueue(command.Command):
    """Purge a queue"""

    _description = _("Purge a queue")
    log = logging.getLogger(__name__ + ".PurgeQueue")

    def get_parser(self, prog_name):
        parser = super(PurgeQueue, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        parser.add_argument(
            "--resource_types",
            metavar="<resource_types>",
            action='append',
            choices=['messages', 'subscriptions'],
            help="Resource types want to be purged.")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        client.queue(queue_name).purge(
            resource_types=parsed_args.resource_types)


class CreatePool(command.ShowOne):
    """Create a pool"""

    _description = _("Create a pool")
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
            "--flavor",
            metavar="<flavor>",
            help="Flavor of the pool")
        parser.add_argument(
            "--pool_options",
            type=json.loads,
            default={},
            metavar="<pool_options>",
            help="An optional request component "
                 "related to storage-specific options")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        kw_arg = {
            'uri': parsed_args.pool_uri,
            'weight': parsed_args.pool_weight,
            'options': parsed_args.pool_options
        }

        if parsed_args.flavor:
            kw_arg.update({'flavor': parsed_args.flavor})

        data = client.pool(parsed_args.pool_name, **kw_arg)

        if not data:
            raise RuntimeError('Failed to create pool(%s).' %
                               parsed_args.pool_name)

        columns = ('Name', 'Weight', 'URI', 'Flavor', 'Options')
        return columns, utils.get_item_properties(data, columns)


class ShowPool(command.ShowOne):
    """Display pool details"""

    _description = _("Display pool details")
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
        client = _get_client(self, parsed_args)

        pool_data = client.pool(parsed_args.pool_name,
                                auto_create=False).get()
        columns = ('Name', 'Weight', 'URI', 'Flavor', 'Options')
        return columns, utils.get_dict_properties(pool_data, columns)


class UpdatePool(command.ShowOne):
    """Update a pool attribute"""

    _description = _("Update a pool attribute")
    log = logging.getLogger(__name__ + ".UpdatePool")

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
            "--flavor",
            metavar="<flavor>",
            help="Flavor of the pool")
        parser.add_argument(
            "--pool_options",
            type=json.loads,
            metavar="<pool_options>",
            help="An optional request component "
                 "related to storage-specific options")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        kw_arg = {}

        if parsed_args.pool_uri:
            kw_arg["uri"] = parsed_args.pool_uri
        if parsed_args.pool_weight:
            kw_arg["weight"] = parsed_args.pool_weight
        if parsed_args.flavor:
            kw_arg["flavor"] = parsed_args.flavor
        if parsed_args.pool_options:
            kw_arg["options"] = parsed_args.pool_options

        pool_obj = client.pool(parsed_args.pool_name, auto_create=False)
        pool_obj.update(kw_arg)
        pool_data = pool_obj.get()
        columns = ('Name', 'Weight', 'URI', 'Flavor', 'Options')
        return columns, utils.get_dict_properties(pool_data, columns)


class DeletePool(command.Command):
    """Delete a pool"""

    _description = _("Delete a pool")
    log = logging.getLogger(__name__ + ".DeletePool")

    def get_parser(self, prog_name):
        parser = super(DeletePool, self).get_parser(prog_name)
        parser.add_argument(
            "pool_name",
            metavar="<pool_name>",
            help="Name of the pool")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        pool_name = parsed_args.pool_name
        client.pool(pool_name, auto_create=False).delete()


class ListPools(command.Lister):
    """List available Pools"""

    _description = _("List available Pools")
    log = logging.getLogger(__name__ + ".ListPools")

    def get_parser(self, prog_name):
        parser = super(ListPools, self).get_parser(prog_name)
        parser.add_argument(
            "--marker",
            metavar="<pool_name>",
            help="Pool's paging marker")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            help="Page size limit")
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="Detailed output")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        kwargs = {}
        columns = ["Name", "Weight", "URI", "Flavor"]
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit
        if parsed_args.detailed is not None and parsed_args.detailed:
            kwargs["detailed"] = parsed_args.detailed
            columns.append("Options")

        data = client.pools(**kwargs)
        columns = tuple(columns)
        return (columns,
                (utils.get_item_properties(s, columns) for s in data))


class DeleteFlavor(command.Command):
    """Delete a pool flavor"""

    _description = _("Delete a pool flavor")
    log = logging.getLogger(__name__ + ".DeleteFlavor")

    def get_parser(self, prog_name):
        parser = super(DeleteFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "flavor_name",
            metavar="<flavor_name>",
            help="Name of the flavor")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        flavor_name = parsed_args.flavor_name
        client.flavor(flavor_name, auto_create=False).delete()


class ShowFlavor(command.ShowOne):
    """Display pool flavor details"""

    _description = _("Display pool flavor details")
    log = logging.getLogger(__name__ + ".ShowFlavor")

    def get_parser(self, prog_name):
        parser = super(ShowFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "flavor_name",
            metavar="<flavor_name>",
            help="Flavor to display (name)",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        client = self.app.client_manager.messaging
        flavor_data = client.flavor(parsed_args.flavor_name,
                                    auto_create=False).get()
        columns = ('Name', 'Pool list', 'Capabilities')
        return columns, utils.get_dict_properties(flavor_data, columns)


class ListFlavors(command.Lister):
    """List available pool flavors"""

    _description = _("List available pool flavors")
    log = logging.getLogger(__name__ + ".ListFlavors")

    def get_parser(self, prog_name):
        parser = super(ListFlavors, self).get_parser(prog_name)
        parser.add_argument(
            "--marker",
            metavar="<flavor_name>",
            help="Flavor's paging marker")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            help="Page size limit")
        parser.add_argument(
            "--detailed",
            action="store_true",
            help="If show detailed capabilities of flavor")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        kwargs = {'detailed': parsed_args.detailed}
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit
        data = client.flavors(**kwargs)
        columns = ("Name", 'Pool list')
        if parsed_args.detailed:
            columns = ("Name", 'Pool list', 'Capabilities')
        return (columns,
                (utils.get_item_properties(s, columns) for s in data))


class UpdateFlavor(command.ShowOne):
    """Update a flavor's attributes"""

    _description = _("Update a flavor's attributes")
    log = logging.getLogger(__name__ + ".UpdateFlavor")

    def get_parser(self, prog_name):
        parser = super(UpdateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "flavor_name",
            metavar="<flavor_name>",
            help="Name of the flavor")
        parser.add_argument(
            "--pool_list",
            metavar="<pool_list>",
            help="Pool list the flavor sits on")
        parser.add_argument(
            "--capabilities",
            metavar="<capabilities>",
            type=json.loads,
            help="Describes flavor-specific capabilities.")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        client = self.app.client_manager.messaging
        kwargs = {}
        if parsed_args.pool_list:
            pool_list = parsed_args.pool_list.split(',')
            kwargs['pool_list'] = pool_list
        if parsed_args.capabilities:
            kwargs['capabilities'] = json.loads(parsed_args.capabilities)

        flavor = client.flavor(parsed_args.flavor_name, auto_create=False)
        columns = ('Name', 'Pool_list', 'Capabilities')
        flavor.update(kwargs)
        flavor_data = flavor.get()
        return columns, utils.get_dict_properties(flavor_data, columns)


class CreateFlavor(command.ShowOne):
    """Create a pool flavor"""

    _description = _("Create a pool flavor")
    log = logging.getLogger(__name__ + ".CreateFlavor")

    def get_parser(self, prog_name):
        parser = super(CreateFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "flavor_name",
            metavar="<flavor_name>",
            help="Name of the flavor")
        parser.add_argument(
            "--pool_list",
            metavar="<pool_list>",
            help="Pool list for flavor")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        pool_list = None
        if parsed_args.pool_list:
            pool_list = parsed_args.pool_list.split(',')
        data = client.flavor(parsed_args.flavor_name,
                             pool_list=pool_list)

        columns = ('Name', 'Pool list', 'Capabilities')
        return columns, utils.get_item_properties(data, columns)


class CreateSubscription(command.ShowOne):
    """Create a subscription for queue"""

    _description = _("Create a subscription for queue")
    log = logging.getLogger(__name__ + ".CreateSubscription")

    def get_parser(self, prog_name):
        parser = super(CreateSubscription, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue to subscribe to")
        parser.add_argument(
            "subscriber",
            metavar="<subscriber>",
            help="Subscriber which will be notified")
        parser.add_argument(
            "ttl",
            metavar="<ttl>",
            type=int,
            help="Time to live of the subscription in seconds")
        parser.add_argument(
            "--options",
            type=json.loads,
            default={},
            metavar="<options>",
            help="Metadata of the subscription in JSON format")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        kwargs = {'options': parsed_args.options}
        if parsed_args.subscriber:
            kwargs['subscriber'] = parsed_args.subscriber
        if parsed_args.subscriber:
            kwargs['ttl'] = parsed_args.ttl

        data = client.subscription(parsed_args.queue_name, **kwargs)

        if not data:
            raise RuntimeError('Failed to create subscription for (%s).' %
                               parsed_args.subscriber)

        columns = ('ID', 'Subscriber', 'TTL', 'Options')
        return columns, utils.get_item_properties(data, columns)


class UpdateSubscription(command.ShowOne):
    """Update a subscription"""

    _description = _("Update a subscription")
    log = logging.getLogger(__name__ + ".UpdateSubscription")

    def get_parser(self, prog_name):
        parser = super(UpdateSubscription, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue to subscribe to")
        parser.add_argument(
            "subscription_id",
            metavar="<subscription_id>",
            help="ID of the subscription"
        )
        parser.add_argument(
            "--subscriber",
            metavar="<subscriber>",
            help="Subscriber which will be notified")
        parser.add_argument(
            "--ttl",
            metavar="<ttl>",
            type=int,
            help="Time to live of the subscription in seconds")
        parser.add_argument(
            "--options",
            type=json.loads,
            default={},
            metavar="<options>",
            help="Metadata of the subscription in JSON format")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        data = {'subscriber': parsed_args.subscriber,
                'ttl': parsed_args.ttl,
                'options': parsed_args.options}

        kwargs = {'id': parsed_args.subscription_id}
        subscription = client.subscription(parsed_args.queue_name,
                                           auto_create=False, **kwargs)

        subscription.update(data)

        columns = ('ID', 'Subscriber', 'TTL', 'Options')
        return columns, utils.get_item_properties(data, columns)


class DeleteSubscription(command.Command):
    """Delete a subscription"""

    _description = _("Delete a subscription")
    log = logging.getLogger(__name__ + ".DeleteSubscription")

    def get_parser(self, prog_name):
        parser = super(DeleteSubscription, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue for the subscription")
        parser.add_argument(
            "subscription_id",
            metavar="<subscription_id>",
            help="ID of the subscription"
        )
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        client.subscription(parsed_args.queue_name,
                            id=parsed_args.subscription_id,
                            auto_create=False).delete()


class ShowSubscription(command.ShowOne):
    """Display subscription details"""

    _description = _("Display subscription details")
    log = logging.getLogger(__name__ + ".ShowSubscription")

    def get_parser(self, prog_name):
        parser = super(ShowSubscription, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue to subscribe to"
        )
        parser.add_argument(
            "subscription_id",
            metavar="<subscription_id>",
            help="ID of the subscription"
        )
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        kwargs = {'id': parsed_args.subscription_id}
        pool_data = client.subscription(parsed_args.queue_name,
                                        **kwargs)
        columns = ('ID', 'Subscriber', 'TTL', 'Age', 'Confirmed', 'Options')
        return columns, utils.get_dict_properties(pool_data.__dict__, columns)


class ListSubscriptions(command.Lister):
    """List available subscriptions"""

    _description = _("List available subscriptions")
    log = logging.getLogger(__name__ + ".ListSubscriptions")

    def get_parser(self, prog_name):
        parser = super(ListSubscriptions, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue to subscribe to")
        parser.add_argument(
            "--marker",
            metavar="<subscription_id>",
            help="Subscription's paging marker, "
            "the ID of the last subscription of the previous page")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            help="Page size limit, default value is 20")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        kwargs = {'queue_name': parsed_args.queue_name}
        if parsed_args.marker is not None:
            kwargs["marker"] = parsed_args.marker
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit

        data = client.subscriptions(**kwargs)
        columns = ('ID', 'Subscriber', 'TTL', 'Age', 'Confirmed', 'Options')
        return (columns,
                (utils.get_item_properties(s, columns) for s in data))


class CreateClaim(command.Lister):
    """Create claim and return a list of claimed messages"""

    _description = _("Create claim and return a list of claimed messages")
    log = logging.getLogger(__name__ + ".CreateClaim")

    def get_parser(self, prog_name):
        parser = super(CreateClaim, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue to be claim")
        parser.add_argument(
            "--ttl",
            metavar="<ttl>",
            type=int,
            default=300,
            help="Time to live in seconds for claim")
        parser.add_argument(
            "--grace",
            metavar="<grace>",
            type=int,
            default=60,
            help="The message grace period in seconds")
        parser.add_argument(
            "--limit",
            metavar="<limit>",
            type=int,
            default=10,
            help="Claims a set of messages, up to limit")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        kwargs = {}
        if parsed_args.ttl is not None:
            kwargs["ttl"] = parsed_args.ttl
        if parsed_args.grace is not None:
            kwargs["grace"] = parsed_args.grace
        if parsed_args.limit is not None:
            kwargs["limit"] = parsed_args.limit

        queue = client.queue(parsed_args.queue_name, auto_create=False)
        keys = ("claim_id", "id", "ttl", "age", 'body', "checksum")
        columns = ("Claim_ID", "Message_ID", "TTL", "Age", "Messages",
                   "Checksum")
        data = queue.claim(**kwargs)
        return (columns,
                (utils.get_item_properties(s, keys) for s in data))


class QueryClaim(command.Lister):
    """Display claim details"""

    _description = _("Display claim details")
    log = logging.getLogger(__name__ + ".QueryClaim")

    def get_parser(self, prog_name):
        parser = super(QueryClaim, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the claimed queue")
        parser.add_argument(
            "claim_id",
            metavar="<claim_id>",
            help="ID of the claim")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        queue = client.queue(parsed_args.queue_name, auto_create=False)
        keys = ("_id", "age", "ttl", "body")
        columns = ("Message_ID", "Age", "TTL", "Message")
        data = queue.claim(id=parsed_args.claim_id)

        return (columns,
                (utils.get_item_properties(s, keys) for s in data))


class RenewClaim(command.Lister):
    """Renew a claim"""

    _description = _("Renew a claim")
    log = logging.getLogger(__name__ + ".RenewClaim")

    def get_parser(self, prog_name):
        parser = super(RenewClaim, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the claimed queue")
        parser.add_argument(
            "claim_id",
            metavar="<claim_id>",
            help="Claim ID")
        parser.add_argument(
            "--ttl",
            metavar="<ttl>",
            type=int,
            help="Time to live in seconds for claim")
        parser.add_argument(
            "--grace",
            metavar="<grace>",
            type=int,
            help="The message grace period in seconds")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        queue = client.queue(parsed_args.queue_name, auto_create=False)
        kwargs = {}
        if parsed_args.ttl is not None:
            kwargs["ttl"] = parsed_args.ttl
        if parsed_args.grace is not None:
            kwargs["grace"] = parsed_args.grace

        claim_obj = queue.claim(id=parsed_args.claim_id)
        claim_obj.update(**kwargs)
        data = claim_obj
        keys = ("_id", "age", "ttl", "body")
        columns = ("Message_ID", "Age", "TTL", "Message")

        return (columns,
                (utils.get_item_properties(s, keys) for s in data))


class ReleaseClaim(command.Command):
    """Delete a claim"""

    _description = _("Delete a claim")
    log = logging.getLogger(__name__ + ".ReleaseClaim")

    def get_parser(self, prog_name):
        parser = super(ReleaseClaim, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the claimed queue")
        parser.add_argument(
            "claim_id",
            metavar="<claim_id>",
            help="Claim ID to delete")

        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)

        queue = client.queue(parsed_args.queue_name, auto_create=False)
        queue.claim(id=parsed_args.claim_id).delete()


class CreateSignedUrl(command.ShowOne):
    """Create a pre-signed url"""

    _description = _("Create a pre-signed url")
    log = logging.getLogger(__name__ + ".CreateSignedUrl")

    def get_parser(self, prog_name):
        parser = super(CreateSignedUrl, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        parser.add_argument(
            "--paths",
            metavar="<paths>",
            default="messages",
            help="Allowed paths in a comma-separated list. "
                 "Options: messages, subscriptions, claims")
        parser.add_argument(
            "--ttl-seconds",
            metavar="<ttl_seconds>",
            type=int,
            help="Length of time (in seconds) until the signature expires")
        parser.add_argument(
            "--methods",
            metavar="<methods>",
            default="GET",
            help="HTTP methods to allow as a comma-separated list. "
                 "Options: GET, HEAD, OPTIONS, POST, PUT, DELETE")
        return parser

    allowed_paths = ("messages", "subscriptions", "claims")

    def take_action(self, parsed_args):
        client = self.app.client_manager.messaging
        queue = client.queue(parsed_args.queue_name, auto_create=False)

        paths = parsed_args.paths.split(',')
        if not all([p in self.allowed_paths for p in paths]):
            print("Invalid path supplied! Received {}. "
                  "Valid paths are: messages, subscriptions, "
                  "claims".format(','.join(paths)))

        kwargs = {
            'methods': parsed_args.methods.split(','),
            'paths': paths,
        }

        if parsed_args.ttl_seconds:
            kwargs['ttl_seconds'] = parsed_args.ttl_seconds

        data = queue.signed_url(**kwargs)

        fields = ('Paths', 'Methods', 'Expires', 'Signature', 'Project ID')
        return fields, (
            ','.join(data['paths']),
            ','.join(data['methods']),
            data['expires'],
            data['signature'],
            data['project']
        )


class Ping(command.ShowOne):
    """Check if Zaqar server is alive or not"""

    _description = _("Check if Zaqar server is alive or not")
    log = logging.getLogger(__name__ + ".Ping")

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        columns = ('Pingable', )
        return columns, utils.get_dict_properties({'pingable': client.ping()},
                                                  columns)


class Health(command.Command):
    """Display detailed health status of Zaqar server"""

    _description = _("Display detailed health status of Zaqar server")
    log = logging.getLogger(__name__ + ".Health")

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        health = client.health()
        print(json.dumps(health, indent=4, sort_keys=True))


class HomeDoc(command.Command):
    """Display the resource doc of Zaqar server"""

    _description = _("Display detailed resource doc of Zaqar server")
    log = logging.getLogger(__name__ + ".HomeDoc")

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        homedoc = client.homedoc()
        print(json.dumps(homedoc, indent=4, sort_keys=True))
