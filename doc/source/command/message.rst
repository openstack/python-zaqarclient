Health
======

For help on a specific :command:`openstack messaging message` command, enter:

.. code-block:: console

   $ openstack messaging message COMMAND -h/--help

The one command:

.. code-block:: console

      messaging message list
      messaging message post

.. _openstack_messaging_message_list:

openstack messaging message list
--------------------------------

.. code-block:: console

   usage: openstack messaging message list [-h] [-f {csv,json,table,value,yaml}]
                                        [-c COLUMN]
                                        [--quote {all,minimal,none,nonnumeric}]
                                        [--noindent] [--max-width <integer>]
                                        [--fit-width] [--print-empty]
                                        [--sort-column SORT_COLUMN]
                                        [--message-ids <message_ids>]
                                        [--limit <limit>] [--echo]
                                        [--include-claimed]
                                        [--include-delayed]
                                        [--client-id <client_id>]
                                        <queue_name>

List all of the messages in a queue.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

.. _openstack_messaging_message_post:

openstack messaging message post
--------------------------------

.. code-block:: console

   usage: openstack messaging message post [-h] [--client-id <client_id>]
                                        <queue_name> <messages>

Post the messages to a queue.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<messages>``
  messages. It should be json like. For example: '[{"body": "msg", "ttl": 60}]'
