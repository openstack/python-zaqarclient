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


class CreateQueue(cli.CreateQueue):
    """Create a queue"""
    pass


class DeleteQueue(cli.DeleteQueue):
    """Delete a queue"""
    pass


class ListQueues(cli.ListQueues):
    """List available queues"""
    pass


class CheckQueueExistence(cli.CheckQueueExistence):
    """Check queue existence"""
    pass


class SetQueueMetadata(cli.SetQueueMetadata):
    """Set queue metadata"""
    pass


class GetQueueMetadata(cli.GetQueueMetadata):
    """Get queue metadata"""
    pass


class GetQueueStats(cli.GetQueueStats):
    """Get queue stats"""
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
