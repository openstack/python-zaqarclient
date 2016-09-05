# Copyright 2013 Red Hat, Inc.
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

# NOTE(flaper87): Client should be moved to
# an upper package. It's version agnostic.
from zaqarclient.queues.v2 import client

URL = 'http://localhost:8888'


def create_post_delete(queue_name, messages):
    """Simple example

    Creates a queue, posts messages to it
    and finally deletes it.

    :params queue_name: The name of the queue
    :type queue_name: `six.text_type`
    :params messages: Messages to post.
    :type messages: list
    """
    # Note: credential information should be provided
    # using `conf` keyword argument if authentication
    # is enabled at server side. Please refer to
    # keystone_auth.py for more information.
    cli = client.Client(URL, version=2)
    queue = cli.queue(queue_name)
    queue.post(messages)

    for msg in queue.messages(echo=True):
        print(msg.body)
        msg.delete()

    queue.delete()

if __name__ == '__main__':
    messages = [{'body': {'id': idx}, 'ttl': 360}
                for idx in range(20)]
    create_post_delete('my_queue', messages)
