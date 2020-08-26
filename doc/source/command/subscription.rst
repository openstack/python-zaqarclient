Subscription
============

For help on a specific :command:`openstack messaging subscription` command, enter:

.. code-block:: console

   $ openstack messaging subscription COMMAND -h/--help

The ten commands:

.. code-block:: console

      messaging subscription create
      messaging subscription delete
      messaging subscription list
      messaging subscription show
      messaging subscription update

.. _openstack_messaging_subscription_create:

openstack messaging subscription create
---------------------------------------

.. code-block:: console

   usage: openstack messaging subscription create [-h] [-f {json,shell,table,value,yaml}]
                                                  [-c COLUMN] [--max-width <integer>]
                                                  [--noindent] [--prefix PREFIX]
                                                  [--options <options>]
                                                  <queue_name> <subscriber> <ttl>

Create a subscription.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscriber>``
  Subscriber which will be notified.

``<ttl>``
  Time to live of the subscription in seconds.

.. _openstack_messaging_subscription_delete:

openstack messaging subscription delete
---------------------------------------

.. code-block:: console

   usage: openstack messaging subscription delete [-h] <queue_name> <subscription_id>

Delete a subscription.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription.

.. _openstack_messaging_subscription_list:

openstack messaging subscription list
-------------------------------------

.. code-block:: console

   usage: openstack messaging subscription list [-h] [-f {csv,json,table,value,yaml}]
                                                [-c COLUMN] [--max-width <integer>]
                                                [--noindent]
                                                [--quote {all,minimal,none,nonnumeric}]
                                                [--marker <subscription_id>]
                                                [--limit <limit>]
                                                <queue_name>

Get list of subscriptions.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

.. _openstack_messaging_subscription_show:

openstack messaging subscription show
-------------------------------------

.. code-block:: console

   usage: openstack messaging subscription show [-h] [-f {json,shell,table,value,yaml}]
                                                [-c COLUMN] [--max-width <integer>]
                                                [--noindent] [--prefix PREFIX]
                                                <queue_name> <subscription_id>

Query a subscription details.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription.

.. _openstack_messaging_subscription_update:

openstack messaging subscription update
---------------------------------------

.. code-block:: console

   usage: openstack messaging subscription update [-h] [-f {json,shell,table,value,yaml}]
                                                  [-c COLUMN] [--max-width <integer>]
                                                  [--noindent] [--prefix PREFIX]
                                                  [--subscriber <subscriber>] [--ttl <ttl>]
                                                  [--options <options>]
                                                  <queue_name> <subscription_id>

Update a subscription.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription

**Optional arguments:**

``--subscriber <subscriber>``
   Subscriber which will be notified.

``--ttl <ttl>``
  Time to live of the subscription in seconds.

``--options <options>``
  Metadata of the subscription in JSON format.


