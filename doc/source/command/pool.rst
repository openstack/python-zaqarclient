Pool
====

For help on a specific :command:`openstack messaging pool` command, enter:

.. code-block:: console

   $ openstack messaging pool COMMAND -h/--help

The ten commands:

.. code-block:: console

      messaging pool create
      messaging pool delete
      messaging pool list
      messaging pool show
      messaging pool update

.. _openstack_messaging_pool_create:

openstack messaging pool create
-------------------------------

.. code-block:: console

   usage: openstack messaging pool create [-h] [-f {json,shell,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>] [--noindent]
                                          [--prefix PREFIX] [--pool_group <pool_group>]
                                          [--pool_options <pool_options>]
                                          <pool_name> <pool_uri> <pool_weight>

Create a pool.

**Positional arguments:**

``<pool_name>``
  Name of the pool.

``<pool_uri>``
  Storage engine URI.

``<pool_weight>``
  weight of the pool.

**Optional arguments:**

``--pool_group <pool_group>``
  Group of the pool.

``--pool_options <pool_options>``
  An optional request component related to
  storage-specific options.

.. _openstack_messaging_pool_delete:

openstack messaging pool delete
-------------------------------

.. code-block:: console

   usage: openstack messaging pool delete [-h] <pool_name>

Delete a pool.

**Positional arguments:**

``<pool_name>``
  Name of the pool.

.. _openstack_messaging_pool_list:

openstack messaging pool list
-----------------------------

.. code-block:: console

   usage: openstack messaging pool list [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                                        [--max-width <integer>] [--noindent]
                                        [--quote {all,minimal,none,nonnumeric}]
                                        [--marker <pool_name>] [--limit <limit>]
                                        [--detailed <detailed>]

List available Pools.

**Optional arguments:**

``--marker <pool_name>``
  Pool's paging marker.

``--limit <limit>``
  Page size limit.

``--detailed <detailed>``
  Detailed output.

.. _openstack_messaging_pool_show:

openstack messaging pool show
-----------------------------

.. code-block:: console

   usage: openstack messaging pool show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN]
                                        [--max-width <integer>] [--noindent]
                                        [--prefix PREFIX]
                                        <pool_name>

Display pool details.

**Positional arguments:**

``<pool_name>``
  Pool to display (name).

.. _openstack_messaging_pool_update:

openstack messaging pool update
-------------------------------

.. code-block:: console

   usage: openstack messaging pool update [-h] [-f {json,shell,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>] [--noindent]
                                          [--prefix PREFIX] [--pool_uri <pool_uri>]
                                          [--pool_weight <pool_weight>]
                                          [--pool_group <pool_group>]
                                          [--pool_options <pool_options>]
                                          <pool_name>

Update a pool attribute.

**Positional arguments:**

``<pool_name>``
  Name of the pool.

**Optional arguments:**

``--pool_uri <pool_uri>``
  Storage engine URI.

``--pool_weight <pool_weight>``
  Weight of the pool.

``--pool_group <pool_group>``
  Group of the pool.

``--pool_options <pool_options>``
  An optional request component related to
  storage-specific options.

