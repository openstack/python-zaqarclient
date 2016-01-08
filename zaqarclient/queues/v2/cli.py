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

from zaqarclient.queues.v1 import cli

from openstackclient.common import utils


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

        # FIXME(flwang): For now, we still use `pool` though it's not really
        # correct since it's representing `pool_group` actually. But given we
        # will remove pool group soon and get a 1:n mapping for flavor:pool,
        # so let's keep it as it's, just for now.
        kwargs = {}
        if parsed_args.capabilities != {}:
            raise AttributeError("<--capabilities> option is only\
             available in client api version < 2")
        data = client.flavor(parsed_args.flavor_name,
                             pool=parsed_args.pool_group,
                             **kwargs)

        columns = ('Name', 'Pool', 'Capabilities')
        return columns, utils.get_item_properties(data, columns)


class ListFlavors(cli.ListFlavors):
    """List available flavors"""
    pass
