# Copyright 2016 Catalyst IT Ltd
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

from zaqarclient.queues.v2 import client

URL = 'http://localhost:8888'


def create_post_delete(queue_name, messages):
    """Presigned queue example

    Creates a queue, posts messages to it and finally deletes it with
    ``signed-url`` auth strategy enabled on Zaqar server side.

    :params queue_name: The name of the queue
    :type queue_name: str
    :params messages: Messages to post.
    :type messages: list
    """
    conf = {'auth_opts':
            {'backend': 'signed-url',
             'options': {'signature': '',
                         'expires': '',
                         'methods': ['GET', 'PATCH', 'POST', 'PUT'],
                         'paths': ['/v2/queues/beijing/claims'],
                         'os_project_id': '2887aabf368046a3bb0070f1c0413470'}
             }
            }
    cli = client.Client(URL, conf=conf)
    queue = cli.queue(queue_name)
    queue.post(messages)

    for msg in queue.messages(echo=True):
        print(msg.body)
        msg.delete()


if __name__ == '__main__':
    messages = [{'body': {'id': idx}, 'ttl': 360}
                for idx in range(20)]
    create_post_delete('beijing', messages)
