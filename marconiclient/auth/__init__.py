# Copyright (c) 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo.config import cfg

from marconiclient.auth import base

_BACKENDS = {
    'noauth': base.NoAuth,
}


def _register_opts(conf):
    """Registers auth cli options.

    This function exists mostly for testing
    purposes.
    """
    backend_opt = cfg.StrOpt('auth_backend', default='noauth',
                             help='Backend plugin to use for authentication')
    conf.register_cli_opt(backend_opt)


def get_backend(conf):
    _register_opts(conf)
    backend = _BACKENDS[conf.auth_backend](conf)
    return backend
