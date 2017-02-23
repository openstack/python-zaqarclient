# Copyright (c) 2015 Catalyst IT Ltd.
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

from zaqarclient.queues.v2 import core


class Subscription(object):

    def __init__(self, client, queue_name, subscriber=None, ttl=60, id=None,
                 auto_create=True, **kwargs):
        self.client = client

        self.id = id
        self.queue_name = queue_name
        self.subscriber = subscriber
        self.ttl = ttl
        self.options = kwargs.get('options', {})
        self.age = kwargs.get('age')
        self.confirmed = kwargs.get('confirmed')

        if auto_create:
            self.ensure_exists()

    def ensure_exists(self):
        """Ensures subscription exists

        This method is not race safe, the subscription could've been deleted
        right after it was called.
        """
        req, trans = self.client._request_and_transport()

        if not self.id and self.subscriber:
            subscription_data = {'subscriber': self.subscriber,
                                 'ttl': self.ttl,
                                 'options': self.options
                                 }
            subscription = core.subscription_create(trans, req,
                                                    self.queue_name,
                                                    subscription_data)

            if subscription and 'subscription_id' in subscription:
                self.id = subscription['subscription_id']

        if self.id:
            sub = core.subscription_get(trans, req, self.queue_name, self.id)
            self.subscriber = sub.get('subscriber')
            self.ttl = sub.get('ttl')
            self.options = sub.get('options')
            self.age = sub.get('age')
            self.confirmed = sub.get('confirmed')

    def update(self, subscription_data):
        req, trans = self.client._request_and_transport()
        core.subscription_update(trans, req, self.queue_name,
                                 self.id, subscription_data)

        for key, value in subscription_data.items():
            setattr(self, key, value)

    def delete(self):
        req, trans = self.client._request_and_transport()
        core.subscription_delete(trans, req, self.queue_name, self.id)


def create_object(parent):
    return lambda kwargs: Subscription(parent, kwargs.pop('source'),
                                       subscriber=kwargs.pop('subscriber'),
                                       ttl=kwargs.pop('ttl'),
                                       id=kwargs.pop('id'),
                                       age=kwargs.pop('age'),
                                       confirmed=kwargs.pop('confirmed'),
                                       auto_create=False,
                                       **kwargs)
