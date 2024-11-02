Flavor
======

For help on a specific :command:`openstack messaging flavor` command, enter:

.. code-block:: console

   $ openstack messaging flavor COMMAND -h/--help

The five commands:

.. code-block:: console

      messaging flavor create
      messaging flavor delete
      messaging flavor list
      messaging flavor show
      messaging flavor update

.. _openstack_messaging_flavor_create:

openstack messaging flavor create
---------------------------------

.. code-block:: console

   usage: openstack messaging flavor create [-h]
                                            [-f {json,shell,table,value,yaml}]
                                            [-c COLUMN] [--max-width <integer>]
                                            [--noindent] [--prefix PREFIX]
                                            [--capabilities <capabilities>]
                                            <flavor_name> <pool_group>

Create a pool flavor.

**Positional arguments:**

``<flavor_name>``
  Name of the flavor.

``<pool_group>``
  Pool group for flavor.

**Optional arguments:**

``--capabilities <capabilities>``
  Describes flavor-specific capabilities,
  This option is only available in client api version < 2.

.. _openstack_messaging_flavor_delete:

openstack messaging flavor delete
---------------------------------

.. code-block:: console

   usage: openstack messaging flavor delete [-h] <flavor_name>

Delete a pool flavor.

**Positional arguments:**

``<flavor_name>``
  Name of the flavor.

.. _openstack_messaging_flavor_list:

openstack messaging flavor list
-------------------------------

.. code-block:: console

   usage: openstack messaging flavor list [-h] [-f {csv,json,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>]
                                          [--noindent]
                                          [--quote {all,minimal,none,nonnumeric}]
                                          [--marker <flavor_name>]
                                          [--limit <limit>]
                                          [--detailed <detailed>]

List available pool flavors.

**Optional arguments:**

``--marker <flavor_name>``
  Flavor's paging marker.

``--limit <limit>``
  Page size limit.

``--detailed <detailed>``
  If show detailed capabilities of flavor.

.. _openstack_messaging_flavor_show:

openstack messaging flavor show
-------------------------------

.. code-block:: console

   usage: openstack messaging flavor show [-h] [-f {json,shell,table,value,yaml}]
                                          [-c COLUMN] [--max-width <integer>]
                                          [--noindent] [--prefix PREFIX]
                                          <flavor_name>

Display flavor details.

**Positional arguments:**

``<flavor_name>``
  Flavor to display (name).

.. _openstack_messaging_flavor_update:

openstack messaging flavor update
---------------------------------

.. code-block:: console

   usage: openstack messaging flavor update [-h]
                                            [-f {json,shell,table,value,yaml}]
                                            [-c COLUMN] [--max-width <integer>]
                                            [--noindent] [--prefix PREFIX]
                                            [--pool_group <pool_group>]
                                            [--capabilities <capabilities>]
                                            <flavor_name>

Update a pool flavor's attributes.

**Positional arguments:**

``<flavor_name>``
  Name of the flavor.

**Optional arguments:**

``--pool_group <pool_group>``
  Pool group the flavor sits on.

``--capabilities <capabilities>``
  Describes flavor-specific capabilities.
