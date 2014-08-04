# Copyright 2013 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__all__ = ['ZaqarError', 'DriverLoadFailure', 'InvalidOperation']


class ZaqarError(Exception):
    """Base class for errors."""


class DriverLoadFailure(ZaqarError):
    """Raised if a transport driver can't be loaded."""

    def __init__(self, driver, ex):
        msg = 'Failed to load transport driver "%s": %s' % (driver, ex)
        super(DriverLoadFailure, self).__init__(msg)
        self.driver = driver
        self.ex = ex


class InvalidOperation(ZaqarError):
    """Raised when attempted a non existent operation."""
