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
"""
A `Client` is a high-level abstraction on top of Zaqar features. It
exposes the server features with an object-oriented interface, which
encourages dot notation and automatic, but lazy, resources
allocation. A `Client` allows you to control everything, from public
interfaces to admin endpoints.

To create a `Client` instance, you supply an url pointing to the
server and a version number::

    from zaqarclient.queues import client

    cli = client.Client(\'http://zaqar.example.com:8888/\', version=2)

which will load the appropriate client based on the specified
version. Optionally, you can also supply a config dictionary::

    from zaqarclient.queues import client

    cli = client.Client(\'http://zaqar.example.com:8888/\',
                        version=2, conf={})

The arguments passed to this function will be passed to the client
instances as well.

It's recommended to use `Client` instances instead of accessing the
lower level API as it has been designed to ease the interaction with
the server and it gives enough control for the most common cases.

A simple example for accessing an existing queue through a client
instance - based on the API v2 - would look like::

    from zaqarclient.queues import client

    cli = client.Client(\'http://zaqar.example.com:8888/\', version=2)
    queue = cli.queue(\'my_queue\')

Through the queue instance will be then possible to access all the
features associated with the queue itself like posting messages,
getting message and deleting messages.

As mentioned previously in this documentation, a client instance
allows you to also access admin endpoints, for example::

    from zaqarclient.queues import client

    cli = client.Client(\'http://zaqar.example.com:8888/\', version=2)
    flavor = cli.flavor(\'tasty\',
                        pool=\'my-pool-group\',
                        auto_create=True)
    flavor.delete()

`Client` uses the lower-level API to access the server, which means
anything you can do with this client instance can be done by accessing
the underlying API, although not recommended.
"""
from zaqarclient import errors
from zaqarclient.queues.v1 import client as cv1
from zaqarclient.queues.v2 import client as cv2

_CLIENTS = {1: cv1.Client,
            1.1: cv1.Client,
            2: cv2.Client}


def Client(url=None, version=None, conf=None, session=None):
    # NOTE: Please don't mix use the Client object with different version at
    # the same time. Because the cache mechanism of queue's metadata will lead
    # to unexpected response value.
    # Please see zaqarclient.queues.v1.queues.Queue.metadata and
    # zaqarclient.queues.v2.queues.Queue.metadata for more detail.
    try:
        return _CLIENTS[version](url=url, version=version, conf=conf,
                                 session=session)
    except KeyError:
        raise errors.ZaqarError('Unknown client version')
