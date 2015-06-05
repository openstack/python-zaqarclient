*******************
Python Zaqar Client
*******************

:version: 0.1.0
:Wiki: `Zaqar Wiki`_
:Launchpad: `Zaqar Launchpad`_
:Review: `Code Review`_
:Design: `Client Wiki`_
:IRC: #openstack-zaqar @ freenode

Welcome to the `Zaqar`_ Python Client project!

**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none

============
Installation
============

The latest stable release can be installed from PyPI::

    pip install --upgrade python-zaqarclient

For the adventurous, you may also install the latest code directly from GitHub::

    pip install git+https://github.com/openstack/python-zaqarclient.git

=================
What's in the box
=================

By installing python-zaqarclient you get programmatic access to the Zaqar v1.0
API library. Plus, it installs a plugin to python-openstackclient that allows
you to perform simple queue operations.

==========
How to use
==========

-------------
Python client
-------------

Details about design, features, usage and workflow can be found in the
`Python Client Wiki`_.

.. _Python Client Wiki: https://wiki.openstack.org/wiki/Zaqar/PythonClient

----------------------
Command line interface
----------------------

Zaqar bases its client implementation in the `OpenStack Client`_. It can be
installed and configured by following the instructions in `Getting Started`_
and `Configuration`_ in the OpenStack Client readme respectively.

The CLI currently allows creation, removal and listing of queues. Some examples
are::

    $  openstack queue list --limit 3
    $  openstack queue create myqueue
    $  openstack queue delete myqueue

.. _`OpenStack Client`: https://github.com/openstack/python-openstackclient
.. _`Getting Started`: https://github.com/openstack/python-openstackclient#getting-started
.. _`Configuration`: https://github.com/openstack/python-openstackclient#configuration

============
Contributing
============

Be sure to reference the `HACKING`_ file for details on coding style. You may
also wish to read through Zaqar's `Contributor Guide`_ before contributing your
first patch.

.. _Zaqar: https://github.com/openstack/zaqar
.. _HACKING: https://github.com/openstack/python-zaqarclient/tree/master/HACKING.rst
.. _Zaqar Wiki: https://wiki.openstack.org/wiki/Zaqar
.. _Contributor Guide: https://wiki.openstack.org/wiki/Zaqar#Contributor_Guide
.. _Zaqar Launchpad: https://launchpad.net/zaqar
.. _Code Review: https://review.openstack.org/#/q/status:open+project:openstack/python-zaqarclient,n,z
.. _Client Wiki: https://wiki.openstack.org/wiki/Python_Zaqar_Client


* License: Apache License, Version 2.0
* Source: http://git.openstack.org/cgit/openstack/python-zaqarclient
* Bugs: http://bugs.launchpad.net/python-zaqarclient
