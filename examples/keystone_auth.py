# Copyright 2014 Red Hat, Inc.
# Copyright 2014 IBM Corp.
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
    """Auth example

    Creates a queue, posts messages to it and finally deletes it with
    keystone auth strategy enabled on Zaqar server side.

    :params queue_name: The name of the queue
    :type queue_name: `six.text_type`
    :params messages: Messages to post.
    :type messages: list
    """
    conf = {'auth_opts':
            {'backend': 'keystone',
             'options': {'os_username': 'zaqar',
                         'os_password': 'zaqar',
                         'os_project_id': 'ccad479c402f43a2994f6e372ab3f8fe',
                         'os_project_name': '',
                         'os_auth_url': 'http://127.0.0.1:5000/v2.0/',
                         'insecure': ''}
             }
            }
    cli = client.Client(URL, conf=conf)
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
