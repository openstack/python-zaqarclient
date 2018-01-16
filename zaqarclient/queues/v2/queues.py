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

from zaqarclient.queues.v1 import queues
from zaqarclient.queues.v2 import claim as claim_api
from zaqarclient.queues.v2 import core
from zaqarclient.queues.v2 import message


class Queue(queues.Queue):

    message_module = message

    def signed_url(self, paths=None, ttl_seconds=None, methods=None):
        req, trans = self.client._request_and_transport()
        return core.signed_url_create(trans, req, self._name, paths=paths,
                                      ttl_seconds=ttl_seconds, methods=methods)

    def subscriptions(self, detailed=False, marker=None, limit=20):
        return self.client.subscriptions(queue_name=self._name,
                                         detailed=detailed,
                                         marker=marker,
                                         limit=limit)

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
