*********************
Python Marconi Client
*********************

:version: 0.1.0
:Wiki: `Marconi Wiki`_
:Launchpad: `Marconi Launchpad`_
:Review: `Code Review`_
:Design: `Client Wiki`_
:IRC: #openstack-marconi @ freenode

Welcome to the `Marconi`_ Python Client project!

**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none

============
Installation
============

The latest stable release can be installed from PyPI::

    pip install --upgrade python-marconiclient

For the adventurous, you may also install the latest code directly from GitHub::

    pip install git+https://github.com/openstack/python-marconiclient.git

=================
What's in the box
=================

By installing python-marconiclient you get programmatic access to the Marconi v1.0 API library. Plus, it installs a plugin to python-openstackclient that allows you to perform simple queue operations.

==========
How to use
==========

-------------
Python client
-------------

Details about design, features, usage and workflow can be found in the `Python Client Wiki`_.

.. _Python Client Wiki: https://wiki.openstack.org/wiki/Marconi/PythonClient

----------------------
Command line interface
----------------------

Marconi bases its client implementation in the `OpenStack Client`_. It can be installed and configured by following the instructions in `Getting Started`_ and `Configuration`_ in the OpenStack Client readme respectively.

The CLI currently allows creation, removal and listing of queues. Some examples are:

    $  openstack queue list --limit 3
    $  openstack queue create myqueue
    $  openstack queue delete myqueue

.. _`OpenStack Client`: https://github.com/openstack/python-openstackclient
.. _`Getting Started`: https://github.com/openstack/python-openstackclient#getting-started
.. _`Configuration`: https://github.com/openstack/python-openstackclient#configuration

============
Contributing
============

Be sure to reference the `HACKING`_ file for details on coding style. You may also wish to read through Marconi's `Contributor Guide`_ before contributing your first patch.

.. _Marconi: https://github.com/openstack/marconi
.. _HACKING: https://github.com/openstack/python-marconiclient/tree/master/HACKING.rst
.. _Marconi Wiki: https://wiki.openstack.org/wiki/Marconi
.. _Contributor Guide: https://wiki.openstack.org/wiki/Marconi#Contributor_Guide
.. _Marconi Launchpad: https://launchpad.net/marconi
.. _Code Review: https://review.openstack.org/#/q/status:open+project:openstack/python-marconiclient,n,z
.. _Client Wiki: https://wiki.openstack.org/wiki/Python_Marconi_Client
