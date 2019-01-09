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


class OldCreateQueue(CreateQueue):
    """Create a queue"""

    _description = _("Create a queue")
    # TODO(wanghao): Remove this class and ``queue create`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue create" instead.'))
        return super(OldCreateQueue, self).take_action(parsed_args)


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


class OldDeleteQueue(DeleteQueue):
    """Delete a queue"""

    _description = _("Delete a queue")
    # TODO(wanghao): Remove this class and ``queue delete`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue delete" instead.'))
        return super(OldDeleteQueue, self).take_action(parsed_args)


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

        data = client.queues(**kwargs)
        columns = tuple(columns)
        return (columns, (utils.get_item_properties(s, columns) for s in data))


class OldListQueues(ListQueues):
    """List available queues"""

    _description = _("List available queues")
    # TODO(wanghao): Remove this class and ``queue list`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue list" instead.'))
        return super(OldListQueues, self).take_action(parsed_args)


class CheckQueueExistence(command.ShowOne):
    """Check queue existence"""

    _description = _("Check queue existence")
    log = logging.getLogger(__name__ + ".CheckQueueExistence")

    def get_parser(self, prog_name):
        parser = super(CheckQueueExistence, self).get_parser(prog_name)
        parser.add_argument(
            "queue_name",
            metavar="<queue_name>",
            help="Name of the queue")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        queue = client.queue(queue_name, auto_create=False)

        columns = ('Exists',)
        data = dict(exists=queue.exists())
        return columns, utils.get_dict_properties(data, columns)


class OldQueueExistence(CheckQueueExistence):
    """Check queue existence"""

    _description = _("Check queue existence")
    # TODO(wanghao): Remove this class and ``queue exists`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue exists" instead.'))
        return super(OldQueueExistence, self).take_action(parsed_args)


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
            help="Queue metadata")
        return parser

    def take_action(self, parsed_args):
        client = _get_client(self, parsed_args)
        queue_name = parsed_args.queue_name
        queue_metadata = parsed_args.queue_metadata
        if (client.api_version == 1 and
                not client.queue(queue_name, auto_create=False).exists()):
            raise RuntimeError("Queue(%s) does not exist." % queue_name)

        try:
            valid_metadata = json.loads(queue_metadata)
        except ValueError:
            raise RuntimeError("Queue metadata(%s) is not a valid json." %
                               queue_metadata)

        client.queue(queue_name, auto_create=False).\
            metadata(new_meta=valid_metadata)


class OldSetQueueMetadata(SetQueueMetadata):
    """Set queue metadata"""

    _description = _("Set queue metadata")
    # TODO(wanghao): Remove this class and ``queue set metadata`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue set metadata" '
                           'instead.'))
        return super(OldSetQueueMetadata, self).take_action(parsed_args)


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

        if client.api_version == 1 and not queue.exists():
            raise RuntimeError("Queue(%s) does not exist." % queue_name)

        columns = ("Metadata",)
        data = dict(metadata=queue.metadata())
        return columns, utils.get_dict_properties(data, columns)


class OldGetQueueMetadata(GetQueueMetadata):
    """Get queue metadata"""

    _description = _("Get queue metadata")
    # TODO(wanghao): Remove this class and ``queue get metadata`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue get metadata" '
                           'instead.'))
        return super(OldGetQueueMetadata, self).take_action(parsed_args)


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


class OldGetQueueStats(GetQueueStats):
    """Get queue stats"""

    _description = _("Get queue stats")
    # TODO(wanghao): Remove this class and ``queue stats`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging queue stats" '
                           'instead.'))
        return super(OldGetQueueStats, self).take_action(parsed_args)


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


class OldCreatePool(CreatePool):
    """Create a pool"""

    _description = _("Create a pool")
    # TODO(wanghao): Remove this class and ``pool create`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging pool create" '
                           'instead.'))
        return super(OldCreatePool, self).take_action(parsed_args)


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


class OldShowPool(ShowPool):
    """Display pool details"""

    _description = _("Display pool details")
    # TODO(wanghao): Remove this class and ``pool show`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging pool show" '
                           'instead.'))
        return super(OldShowPool, self).take_action(parsed_args)


class UpdatePool(command.ShowOne):
    """Update a pool attribute"""

    _description = _("Update a pool attribute")
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


class OldUpdatePool(UpdatePool):
    """Update a pool attribute"""

    _description = _("Update a pool attribute")
    # TODO(wanghao): Remove this class and ``pool update`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging pool update" '
                           'instead.'))
        return super(OldUpdatePool, self).take_action(parsed_args)


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


class OldDeletePool(DeletePool):
    """Delete a pool"""

    _description = _("Delete a pool")
    # TODO(wanghao): Remove this class and ``pool delete`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging pool delete" '
                           'instead.'))
        return super(OldDeletePool, self).take_action(parsed_args)


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


class OldListPools(ListPools):
    """List available Pools"""

    _description = _("List available Pools")
    # TODO(wanghao): Remove this class and ``pool list`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging pool list" '
                           'instead.'))
        return super(OldListPools, self).take_action(parsed_args)


class UpdateFlavor(command.ShowOne):
    """Update a flavor's attributes"""

    _description = _("Update a flavor's attributes")
    log = logging.getLogger(__name__+".UpdateFlavor")

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
        parser.add_argument(
            "--capabilities",
            metavar="<capabilities>",
            type=json.loads,
            default={},
            help="Describes flavor-specific capabilities, "
                 "This option is only available in client api version < 2 .")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        client = self.app.client_manager.messaging
        kwargs = {'capabilities': parsed_args.capabilities}
        data = client.flavor(parsed_args.flavor_name,
                             pool_list=parsed_args.pool_list,
                             **kwargs)

        columns = ('Name', 'Pool list', 'Capabilities')
        return columns, utils.get_item_properties(data, columns)


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
        keys = ("claim_id", "_id", "ttl", "age", 'body')
        columns = ("Claim_ID", "Message_ID", "TTL", "Age", "Messages")
        data = queue.claim(**kwargs)
        return (columns,
                (utils.get_item_properties(s, keys) for s in data))


class OldCreateClaim(CreateClaim):
    """Create claim and return a list of claimed messages"""

    _description = _("Create claim and return a list of claimed messages")
    # TODO(wanghao): Remove this class and ``claim create`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging claim create" '
                           'instead.'))
        return super(OldCreateClaim, self).take_action(parsed_args)


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


class OldQueryClaim(QueryClaim):
    """Display claim details"""

    _description = _("Display claim details")
    # TODO(wanghao): Remove this class and ``claim query`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging claim query" '
                           'instead.'))
        return super(OldQueryClaim, self).take_action(parsed_args)


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


class OldRenewClaim(RenewClaim):
    """Renew a claim"""

    _description = _("Renew a claim")
    # TODO(wanghao): Remove this class and ``claim renew`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging claim renew" '
                           'instead.'))
        return super(OldRenewClaim, self).take_action(parsed_args)


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


class OldReleaseClaim(ReleaseClaim):
    """Delete a claim"""

    _description = _("Delete a claim")
    # TODO(wanghao): Remove this class and ``claim release`` command
    #                after Queen.

    # This notifies cliff to not display the help for this command
    deprecated = True

    log = logging.getLogger('deprecated')

    def take_action(self, parsed_args):
        self.log.warning(_('This command has been deprecated. '
                           'Please use "messaging claim release" '
                           'instead.'))
        return super(OldReleaseClaim, self).take_action(parsed_args)
