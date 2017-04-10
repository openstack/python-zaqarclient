Queue
=====

For help on a specific :command:`openstack queue` command, enter:

.. code-block:: console

   $ openstack queue COMMAND -h/--help

The seven commands:

.. code-block:: console

      queue create
      queue delete
      queue get metadata
      queue list
      queue set metadata
      queue signed url
      queue stats

.. _openstack_queue_create:

openstack queue create
----------------------

.. code-block:: console

   usage: openstack queue create [-h] [-f {json,shell,table,value,yaml}]
                                 [-c COLUMN] [--max-width <integer>] [--noindent]
                                 [--prefix PREFIX]
                                 <queue_name>

Create a queue.

**Positional arguments:**

``<queue_name>``
  Name of the queue.


.. _openstack_queue_delete:

openstack queue delete
----------------------

.. code-block:: console

   usage: openstack queue delete [-h] <queue_name>

Delete a queue.

**Positional arguments:**

``<queue_name>``
  Name of the queue.


.. _openstack_queue_get_metadata:

openstack queue get metadata
----------------------------

.. code-block:: console

   usage: openstack queue get metadata [-h] [-f {json,shell,table,value,yaml}]
                                       [-c COLUMN] [--max-width <integer>]
                                       [--noindent] [--prefix PREFIX]
                                       <queue_name>

Get queue metadata.

**Positional arguments:**

``<queue_name>``
  Name of the queue.


.. _openstack_queue_list:

openstack queue list
--------------------

.. code-block:: console

   usage: openstack queue list [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                            [--max-width <integer>] [--noindent]
                            [--quote {all,minimal,none,nonnumeric}]
                            [--marker <queue_id>] [--limit <limit>]
                            [--detailed]

List available queues.

**Optional arguments:**

``--marker <queue_id>``
  Queue's paging marker.

``--limit <limit>``
  Page size limit.

``--detailed``
  If show detailed information of queue.


.. _openstack_queue_set_metadata:

openstack queue set metadata
----------------------------

.. code-block:: console

   usage: openstack queue set metadata [-h] <queue_name> <queue_metadata>

Set queue metadata.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

``<queue_metadata>``
  Queue metadata. It should be json like. For example: '{"age": 18}'


.. _openstack_queue_signed_url:

openstack queue signed url
--------------------------

.. code-block:: console

   usage: openstack queue signed url [-h] [-f {json,shell,table,value,yaml}]
                                     [-c COLUMN] [--max-width <integer>]
                                     [--noindent] [--prefix PREFIX]
                                     [--paths <paths>]
                                     [--ttl-seconds <ttl_seconds>]
                                     [--methods <methods>]
                                     <queue_name>

Create a pre-signed url for the queue.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

**Optional arguments:**

``--paths <paths>``
  Allowed paths in a comma-separated list.
  Options: messages, subscriptions, claims.

``--ttl-seconds <ttl_seconds>``
  Length of time (in seconds) until the signature expires.

``--methods <methods>``
  HTTP methods to allow as a comma-separated list.
  Options: GET, HEAD, OPTIONS, POST, PUT, DELETE.


.. _openstack_queue_stats:

openstack queue stats
---------------------

.. code-block:: console

   usage: openstack queue stats [-h] [-f {json,shell,table,value,yaml}]
                                [-c COLUMN] [--max-width <integer>] [--noindent]
                                [--prefix PREFIX]
                                <queue_name>

Get queue stats.

**Positional arguments:**

``<queue_name>``
  Name of the queue.
