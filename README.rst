========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/tc/badges/python-zaqarclient.svg
    :target: http://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

Python Zaqar Client
===================

.. image:: https://img.shields.io/pypi/v/python-zaqarclient.svg
    :target: https://pypi.org/project/python-zaqarclient/
    :alt: Latest Version

:Wiki: `Zaqar Wiki`_
:Launchpad: `Zaqar Launchpad`_
:Review: `Code Review`_
:Design: `Client Wiki`_
:IRC: #openstack-zaqar @ OFTC

Welcome to the `Zaqar`_ Python Client project!

Installation
------------

The latest stable release can be installed from PyPI::

    pip install --upgrade python-zaqarclient

For the adventurous, you may also install the latest code directly from git
.openstack.org::

    pip install git+https://opendev.org/openstack/python-zaqarclient.git

What's in the box
-----------------

By installing python-zaqarclient you get programmatic access to the Zaqar v2.0
API library. Plus, it installs a plugin to python-openstackclient that allows
you to perform simple queue operations.

How to use
==========

Python client
-------------

Details about design, features, usage and workflow can be found in the
`Python Client Wiki`_.

.. _Python Client Wiki: https://wiki.openstack.org/wiki/Zaqar/PythonClient

Command line interface
----------------------

Zaqar bases its client implementation in the `OpenStack Client`_. It can be
installed and configured by following the instructions in *Getting Started*
and *Configuration* in the `OpenStack Client Readme`_ respectively.

The CLI currently allows creation, removal and listing of queues. Some examples
are::

    $  openstack queue list --limit 3
    $  openstack queue create myqueue
    $  openstack queue delete myqueue

.. _`OpenStack Client`: https://opendev.org/openstack/python-openstackclient
.. _`OpenStack Client Readme`: https://opendev.org/openstack/python-openstackclient/src/branch/master/README.rst

Contributing
============

Be sure to reference the `HACKING`_ file for details on coding style. You may
also wish to read through Zaqar's `Contributor Guide`_ before contributing your
first patch.

.. _Zaqar: https://opendev.org/openstack/zaqar
.. _HACKING: https://opendev.org/openstack/python-zaqarclient/src/branch/master/HACKING.rst
.. _Zaqar Wiki: https://wiki.openstack.org/wiki/Zaqar
.. _Contributor Guide: https://wiki.openstack.org/wiki/Zaqar#Contributor_Guide
.. _Zaqar Launchpad: https://launchpad.net/zaqar
.. _Code Review: https://review.opendev.org/q/status:open+project:openstack/python-zaqarclient
.. _Client Wiki: https://wiki.openstack.org/wiki/Python_Zaqar_Client


* License: Apache License, Version 2.0
* `PyPi`_ - package installation
* `Bugs`_ - issue tracking
* `Source`_
* `Release Notes`_

.. _PyPi: https://pypi.org/project/python-zaqarclient
.. _Bugs: https://bugs.launchpad.net/python-zaqarclient
.. _Source: https://opendev.org/openstack/python-zaqarclient/
.. _Release Notes: https://docs.openstack.org/releasenotes/python-zaqarclient

