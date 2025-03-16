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

import re

from zaqarclient._i18n import _  # noqa
from zaqarclient.queues.v2 import claim as claim_api
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import iterator
from zaqarclient.queues.v2 import message

# NOTE(wanghao): This is copied from Zaqar server side, so if server have
# updated it someday, we should update it here to keep consistent.
QUEUE_NAME_REGEX = re.compile(r'^[a-zA-Z0-9_\-]+$')


class Queue(object):

    message_module = message

    def __init__(self, client, name, href=None, metadata=None,
                 auto_create=True, force_create=False):
        """Initialize queue object

        :param client: The client object of Zaqar.
        :type client: `object`
        :param name: Name of the queue.
        :type name: str
        :param href : Hypertext Reference.
        :type href:  str
        :param metadata : A metadata object of the queue.
        :type metadata: `dict`
        :param auto_create: If create the queue automatically in database.
        :type auto_create: `boolean`
        :param force_create: If create the queue and skip the API version
            check, which is useful for command line interface.
        :type force_create: `boolean`
        :returns: The queue object.
        """
        self.client = client

        if name == "":
            raise ValueError(_('Queue name does not have a value'))

        if not QUEUE_NAME_REGEX.match(str(name)):
            raise ValueError(_('The queue name may only contain ASCII '
                               'letters, digits, underscores and dashes.'))

        # NOTE(flaper87) Queue Info
        self._name = name
        self._metadata = metadata
        self._href = href

        # NOTE(flwang): If force_create is True, then even though auto_create
        # is not True, the queue should be created anyway.
        if auto_create or force_create:
            self.ensure_exists(force_create=force_create)

    @property
    def name(self):
        return self._name

    @property
    def href(self):
        return self._href

    @property
    def metadata_dict(self):
        return dict(self.metadata())

    def exists(self):
        """Checks if the queue exists."""
        req, trans = self.client._request_and_transport()
        return core.queue_exists(trans, req, self._name)

    def ensure_exists(self, force_create=False):
        """Ensures a queue exists

        This method is not race safe,
        the queue could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()
        if force_create:
            core.queue_create(trans, req, self._name)

    def metadata(self, new_meta=None, force_reload=False):
        """Get metadata and return it

        :param new_meta: A dictionary containing
            an updated metadata object. If present
            the queue metadata will be updated in
            remote server. If the new_meta is empty,
            the metadata object will be cleared.
        :type new_meta: `dict`
        :param force_reload: Whether to ignored the
            cached metadata and reload it from the
            server.
        :type force_reload: `bool`

        :returns: The queue metadata.
        """
        req, trans = self.client._request_and_transport()

        # TODO(flaper87): Cache with timeout
        if new_meta is None and self._metadata and not force_reload:
            return self._metadata
        else:
            self._metadata = core.queue_get(trans, req, self._name)

        if new_meta is not None:
            temp_metadata = self._metadata.copy()
            changes = []
            for key, value in new_meta.items():
                # If key exists, replace it's value.
                if self._metadata.get(key, None) is not None:
                    changes.append({'op': 'replace',
                                    'path': '/metadata/%s' % key,
                                    'value': value})
                    temp_metadata.pop(key)
                # If not, add the new key.
                else:
                    changes.append({'op': 'add',
                                    'path': '/metadata/%s' % key,
                                    'value': value})
            # For the keys which are not included in the new metadata, remove
            # them.
            for key, value in temp_metadata.items():
                changes.append({'op': 'remove',
                                'path': '/metadata/%s' % key})

            self._metadata = core.queue_update(trans, req, self._name,
                                               metadata=changes)

        return self._metadata

    @property
    def stats(self):
        req, trans = self.client._request_and_transport()
        return core.queue_get_stats(trans, req, self._name)

    def delete(self):
        req, trans = self.client._request_and_transport()
        core.queue_delete(trans, req, self._name)

    # Messages API

    def post(self, messages):
        """Posts one or more messages to this queue

        :param messages: One or more messages to post
        :type messages: `list` or `dict`

        :returns: A dict with the result of this operation.
        :rtype: `dict`
        """
        if not isinstance(messages, list):
            messages = [messages]

        messages = {'messages': messages}

        req, trans = self.client._request_and_transport()

        # TODO(flaper87): Return a list of messages
        return core.message_post(trans, req,
                                 self._name, messages)

    def message(self, message_id):
        """Gets a message by id

        :param message_id: Message's reference
        :type message_id: str

        :returns: A message
        :rtype: `dict`
        """
        req, trans = self.client._request_and_transport()
        msg = core.message_get(trans, req, self._name,
                               message_id)
        return self.message_module.Message(self, **msg)

    def messages(self, *messages, **params):
        """Gets a list of messages from the server

        This method returns a list of messages, it can be
        used to retrieve a set of messages by id or to
        walk through the active messages by using the
        collection endpoint.

        The `messages` and `params` params are mutually exclusive
        and the former has the priority.

        :param messages: List of messages' ids to retrieve.
        :type messages: *args of str

        :param params: Filters to use for getting messages
        :type params: **kwargs dict.

        :returns: List of messages
        :rtype: `list`
        """
        req, trans = self.client._request_and_transport()

        # TODO(flaper87): Return a MessageIterator.
        # This iterator should handle limits, pagination
        # and messages deserialization.

        if messages:
            msgs = core.message_get_many(trans, req,
                                         self._name, messages)
        else:
            # NOTE(flaper87): It's safe to access messages
            # directly. If something wrong happens, the core
            # API will raise the right exceptions.
            msgs = core.message_list(trans, req,
                                     self._name,
                                     **params)

        return iterator._Iterator(self.client,
                                  msgs,
                                  'messages',
                                  self.message_module.create_object(self))

    def delete_messages(self, *messages):
        """Deletes a set of messages from the server

        :param messages: List of messages' ids to delete.
        :type messages: *args of str
        """

        req, trans = self.client._request_and_transport()
        return core.message_delete_many(trans, req, self._name,
                                        set(messages))

    def pop(self, count=1):
        """Pop `count` messages from the server

        :param count: Number of messages to pop.
        :type count: int

        :returns: List of messages
        :rtype: `list`
        """

        req, trans = self.client._request_and_transport()
        msgs = core.message_pop(trans, req, self._name, count=count)
        return iterator._Iterator(self.client,
                                  msgs,
                                  'messages',
                                  self.message_module.create_object(self))

    def signed_url(self, paths=None, ttl_seconds=None, methods=None):
        req, trans = self.client._request_and_transport()
        return core.signed_url_create(trans, req, self._name, paths=paths,
                                      ttl_seconds=ttl_seconds, methods=methods)

    def subscriptions(self, detailed=False, marker=None, limit=20):
        return self.client.subscriptions(queue_name=self._name,
                                         detailed=detailed,
                                         marker=marker,
                                         limit=limit)

    def purge(self, resource_types=None):
        req, trans = self.client._request_and_transport()
        core.queue_purge(trans, req, self._name,
                         resource_types=resource_types)

    def claim(self, id=None, ttl=None, grace=None,
              limit=None):
        return claim_api.Claim(self, id=id, ttl=ttl, grace=grace, limit=limit)


def create_object(parent):
    return lambda args: Queue(parent, args["name"], href=args.get("href"),
                              metadata=args.get("metadata"), auto_create=False)
