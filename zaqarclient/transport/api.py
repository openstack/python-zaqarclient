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

import jsonschema
from jsonschema import validators

from zaqarclient import errors


class Api(object):

    schema = {}
    label = None
    validators = {}

    def is_supported(self, operation):
        """Returns `True` if `operation` is supported

        :param operation: The operation to check on.
        :type operation: str

        :rtype: bool
        """
        return operation in self.schema

    def get_schema(self, operation):
        """Returns the schema for an operation

        :param operation: Operation for which params need
            to be validated.
        :type operation: str

        :returns: Operation's schema
        :rtype: dict

        :raises: `errors.InvalidOperation` if the operation
            does not exist
        """
        try:
            return self.schema[operation]
        except KeyError:
            # TODO(flaper87): gettext support
            msg = '{0} is not a valid operation'.format(operation)
            raise errors.InvalidOperation(msg)

    def validate(self, operation, params):
        """Validates the request data

        This method relies on jsonschema and exists
        just as a way for third-party transport to validate
        the request. It's not recommended to validate every
        request since they are already validated server side.

        :param operation: Operation's for which params need
            to be validated.
        :type operation: str
        :param params: Params to validate
        :type params: dict

        :returns: True if the schema is valid, False otherwise
        :raises: `errors.InvalidOperation` if the operation
            does not exist
        """

        if operation not in self.validators:
            schema = self.get_schema(operation)
            self.validators[operation] = validators.Draft4Validator(schema)

        try:
            self.validators[operation].validate(params)
        except jsonschema.ValidationError:
            # TODO(flaper87): Log error
            return False

        return True
