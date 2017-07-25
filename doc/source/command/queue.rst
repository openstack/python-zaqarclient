Queue
=====

For help on a specific :command:`openstack queue` command, enter:

.. code-block:: console

   $ openstack queue COMMAND -h/--help

The fourteen commands:

.. code-block:: console

      queue create
      messaging queue create
      queue delete
      messaging queue delete
      queue get metadata
      messaging queue get metadata
      queue list
      messaging queue list
      queue set metadata
      messaging queue set metadata
      queue signed url
      messaging queue signed url
      queue stats
      messaging queue stats

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

.. _openstack_messaging_queue_create:

openstack messaging queue create
----------------------

.. code-block:: console

   usage: openstack messaging queue create [-h] [-f {json,shell,table,value,yaml}]
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

.. _openstack_messaging_queue_delete:

openstack messaging queue delete
----------------------

.. code-block:: console

   usage: openstack messaging queue delete [-h] <queue_name>

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

.. _openstack_messaging_queue_get_metadata:

openstack messaging queue get metadata
----------------------------

.. code-block:: console

   usage: openstack messaging queue get metadata [-h] [-f {json,shell,table,value,yaml}]
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

.. _openstack_messaging_queue_list:

openstack messaging queue list
--------------------

.. code-block:: console

   usage: openstack messaging queue list [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
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

.. _openstack_messaging_queue_set_metadata:

openstack messaging queue set metadata
----------------------------

.. code-block:: console

   usage: openstack messaging queue set metadata [-h] <queue_name> <queue_metadata>

Set queue metadata.All the metadata of the queue will be replaced by 
queue_metadata.

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

.. _openstack_messaging_queue_signed_url:

openstack messaging queue signed url
--------------------------

.. code-block:: console

   usage: openstack messaging queue signed url [-h] [-f {json,shell,table,value,yaml}]
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

.. _openstack_messaging_queue_stats:

openstack messaging queue stats
---------------------

.. code-block:: console

   usage: openstack messaging queue stats [-h] [-f {json,shell,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>] [--noindent]
                                          [--prefix PREFIX]
                                          <queue_name>

Get queue stats.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

.. _openstack_queue_purge:

openstack queue purge
---------------------

.. code-block:: console

   usage: openstack queue purge [-h] [--resource_types <resource_types>]
                                <queue_name>

Purge a queue. All the metadata of the queue will be kept. Use
``--resource_types`` to specify which resource should be pured. If
``--resource_types`` is not specified, all the messages and subscriptions in
the queue will be purged by default.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

**Optional arguments:**

``--resource_types <resource_types>`
  Resource types want to be purged. Support ``messages`` and ``subscriptions``.

.. _openstack_messaging_queue_purge:

openstack messaging queue purge
---------------------

.. code-block:: console

   usage: openstack messaging queue purge [-h] [--resource_types <resource_types>]
                                          <queue_name>

Purge a queue. All the metadata of the queue will be kept. Use
``--resource_types`` to specify which resource should be pured. If
``--resource_types`` is not specified, all the messages and subscriptions in
the queue will be purged by default.

**Positional arguments:**

``<queue_name>``
  Name of the queue.

**Optional arguments:**

``--resource_types <resource_types>`
  Resource types want to be purged. Support ``messages`` and ``subscriptions``.
