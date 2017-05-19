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
from zaqarclient.queues.v1 import cli


def _get_client(obj, parsed_args):
    obj.log.debug("take_action(%s)" % parsed_args)
    return obj.app.client_manager.messaging


class CreateQueue(cli.CreateQueue):
    """Create a queue"""
    pass


class DeleteQueue(cli.DeleteQueue):
    """Delete a queue"""
    pass


class ListQueues(cli.ListQueues):
    """List available queues"""
    pass


class GetQueueStats(cli.GetQueueStats):
    """Get queue stats"""
    pass


class SetQueueMetadata(cli.SetQueueMetadata):
    """Set queue metadata"""
    pass


class GetQueueMetadata(cli.GetQueueMetadata):
    """Get queue metadata"""
    pass


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

        queue = client.queue(parsed_args.queue_name)

        if parsed_args.message_ids:
            messages = queue.messages(parsed_args.message_ids.split(','),
                                      **kwargs)
        else:
            messages = queue.messages(**kwargs)

        columns = ("ID", "Body", "TTL", "Age", "Claim ID")
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


class CreatePool(cli.CreatePool):
    """Create a pool"""
    pass


class ShowPool(cli.ShowPool):
    """Display pool details"""
    pass


class UpdatePool(cli.UpdatePool):
    """Update a pool attribute"""
    pass


class DeletePool(cli.DeletePool):
    """Delete a pool"""
    pass


class ListPools(cli.ListPools):
    """List available Pools"""
    pass


class DeleteFlavor(cli.DeleteFlavor):
    """Delete a flavor"""
    pass


class ShowFlavor(cli.ShowFlavor):
    """Display flavor details"""
    pass


class UpdateFlavor(cli.UpdateFlavor):
    """Update a flavor's attributes"""
    pass


class CreateFlavor(cli.CreateFlavor):
    """Create a pool flavor"""

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging

        kwargs = {}
        if parsed_args.capabilities != {}:
            raise AttributeError("<--capabilities> option is only\
             available in client api version < 2")
        data = client.flavor(parsed_args.flavor_name,
                             pool_group=parsed_args.pool_group,
                             **kwargs)

        columns = ('Name', 'Pool Group', 'Capabilities')
        return columns, utils.get_item_properties(data, columns)


class ListFlavors(cli.ListFlavors):
    """List available flavors"""
    pass


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
        subscription = client.subscription(parsed_args.queue_name, kwargs,
                                           auto_create=False)

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
        columns = ('ID', 'Subscriber', 'TTL', 'Options')
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


class CreateClaim(cli.CreateClaim):
    """Create claim and return a list of claimed messages"""
    pass


class QueryClaim(cli.QueryClaim):
    """Display claim details"""
    pass


class RenewClaim(cli.RenewClaim):
    """Renew a claim"""
    pass


class ReleaseClaim(cli.ReleaseClaim):
    """Delete a claim"""
    pass


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
