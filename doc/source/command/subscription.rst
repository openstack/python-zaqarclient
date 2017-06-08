Subscription
============

For help on a specific :command:`openstack subscription` command, enter:

.. code-block:: console

   $ openstack subscription COMMAND -h/--help

The ten commands:

.. code-block:: console

      subscription create
      messaging subscription create
      subscription delete
      messaging subscription delete
      subscription list
      messaging subscription list
      subscription show
      messaging subscription show
      subscription update
      messaging subscription update

.. _openstack_subscription_create:

openstack subscription create
-----------------------------

.. code-block:: console

   usage: openstack subscription create [-h] [-f {json,shell,table,value,yaml}]
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

.. _openstack_messaging_subscription_create:

openstack messaging subscription create
-----------------------------

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

.. _openstack_subscription_delete:

openstack subscription delete
-----------------------------

.. code-block:: console

   usage: openstack subscription delete [-h] <queue_name> <subscription_id>

Delete a subscription.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription.

.. _openstack_messaging_subscription_delete:

openstack messaging subscription delete
-----------------------------

.. code-block:: console

   usage: openstack messaging subscription delete [-h] <queue_name> <subscription_id>

Delete a subscription.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription.

.. _openstack_subscription_list:

openstack subscription list
---------------------------

.. code-block:: console

   usage: openstack subscription list [-h] [-f {csv,json,table,value,yaml}]
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

.. _openstack_messaging_subscription_list:

openstack messaging subscription list
---------------------------

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

.. _openstack_subscription_show:

openstack subscription show
---------------------------

.. code-block:: console

   usage: openstack subscription show [-h] [-f {json,shell,table,value,yaml}]
                                      [-c COLUMN] [--max-width <integer>]
                                      [--noindent] [--prefix PREFIX]
                                      <queue_name> <subscription_id>

Query a subscription details.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<subscription_id>``
  ID of the subscription.

.. _openstack_messaging_subscription_show:

openstack messaging subscription show
---------------------------

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

.. _openstack_subscription_update:

openstack subscription update
-----------------------------

.. code-block:: console

   usage: openstack subscription update [-h] [-f {json,shell,table,value,yaml}]
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

.. _openstack_messaging_subscription_update:

openstack messaging subscription update
-----------------------------

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


