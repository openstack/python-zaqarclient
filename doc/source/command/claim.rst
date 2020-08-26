Claim
=====

For help on a specific :command:`openstack messaging claim` command, enter:

.. code-block:: console

   $ openstack messaging claim COMMAND -h/--help

The eight commands:

.. code-block:: console

      messaging claim create
      messaging claim query
      messaging claim release
      messaging claim renew

.. _openstack_messaging_claim_create:

openstack messaging claim create
--------------------------------

.. code-block:: console

   usage: openstack messaging claim create [-h] [-f {csv,json,table,value,yaml}]
                                           [-c COLUMN] [--max-width <integer>] [--noindent]
                                           [--quote {all,minimal,none,nonnumeric}]
                                           [--ttl <ttl>] [--grace <grace>]
                                           [--limit <limit>]
                                           <queue_name>

Create claim and return a list of claimed messages.

**Positional arguments:**

``<queue_name>``
  Name of the queue to be claim.

**Optional arguments:**

``--ttl <ttl>``
  Time to live in seconds for claim.

``--grace <grace>``
  The message grace period in seconds.

``--limit <limit>``
  Claims a set of messages, up to limit.

.. _openstack_messaging_claim_query:

openstack messaging claim query
-------------------------------

.. code-block:: console

   usage: openstack messaging claim query [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                          [--max-width <integer>] [--noindent]
                                          [--quote {all,minimal,none,nonnumeric}]
                                          <queue_name> <claim_id>

Display claim details.

**Positional arguments:**

``<queue_name>``
  Name of the claimed queue.

``<claim_id>``
  ID of the claim.

.. _openstack_messaging_claim_release:

openstack messaging claim release
---------------------------------

.. code-block:: console

   usage: openstack messaging claim release [-h] <queue_name> <claim_id>

Delete a claim.

**Positional arguments:**

``<queue_name>``
  Name of the claimed queue.

``<claim_id>``
  Claim ID to delete.

.. _openstack_messaging_claim_renew:

openstack messaging claim renew
-------------------------------

.. code-block:: console

   usage: openstack messaging claim renew [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                          [--max-width <integer>] [--noindent]
                                          [--quote {all,minimal,none,nonnumeric}]
                                          [--ttl <ttl>] [--grace <grace>]
                                          <queue_name> <claim_id>

Renew a claim.

**Positional arguments:**

``<queue_name>``
  Name of the claimed queue.

``<claim_id>``
  Claim ID.

**Optional arguments:**

``--ttl <ttl>``
  Time to live in seconds for claim.

``--grace <grace>``
  The message grace period in seconds.
