Claim
=====

For help on a specific :command:`openstack claim` command, enter:

.. code-block:: console

   $ openstack claim COMMAND -h/--help

The four commands:

.. code-block:: console

      claim create
      claim query
      claim release
      claim renew

.. _openstack_claim_create:

openstack claim create
----------------------

.. code-block:: console

   usage: openstack claim create [-h] [-f {csv,json,table,value,yaml}]
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


.. _openstack_claim_query:

openstack claim query
---------------------

.. code-block:: console

   usage: openstack claim query [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                [--max-width <integer>] [--noindent]
                                [--quote {all,minimal,none,nonnumeric}]
                                <queue_name> <claim_id>

Display claim details.

**Positional arguments:**

``<queue_name>``
  Name of the claimed queue.

``<claim_id>``
  ID of the claim.

.. _openstack_claim_release:

openstack claim release
-----------------------

.. code-block:: console

   usage: openstack claim release [-h] <queue_name> <claim_id>

Delete a claim.

**Positional arguments:**

``<queue_name>``
  Name of the claimed queue.

``<claim_id>``
  Claim ID to delete.

.. _openstack_claim_renew:

openstack claim renew
---------------------

.. code-block:: console

   usage: openstack claim renew [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                [--max-width <integer>] [--noindent]
                                [--quote {all,minimal,none,nonnumeric}]
                                [--ttl <ttl>] [--grace <grace>]
                                <queue_name> <claim_id>

Renew a claim.

**Positional arguments:**

``<queue_name> ``
  Name of the claimed queue.

``<claim_id>``
  Claim ID.

**Optional arguments:**

``--ttl <ttl>``
  Time to live in seconds for claim.

``--grace <grace>``
  The message grace period in seconds.
