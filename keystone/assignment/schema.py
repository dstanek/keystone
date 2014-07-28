# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystone.common.validation import parameter_types

import jsd


class ProjectSchema(jsd.Object):
    # required
    domain_id = parameter_types.IdString(required=True)
    name = parameter_types.Name(required=True)

    # optional
    description = parameter_types.Description()
    enabled = parameter_types.Boolean()


domain_create = {
    'type': 'object',
    'properties': {
        'description': parameter_types.description,
        'enabled': parameter_types.boolean,
        'name': parameter_types.name
    },
    'required': ['name'],
    'additionalProperties': True
}

domain_update = {
    'type': 'object',
    'properties': {
        'description': parameter_types.description,
        'enabled': parameter_types.boolean,
        'name': parameter_types.name
    },
    'minProperties': 1,
    'additionalProperties': True
}

role_create = {
    'type': 'object',
    'properties': {
        'name': parameter_types.name
    },
    'required': ['name'],
    'additionalProperties': True
}

role_update = {
    'type': 'object',
    'properties': {
        'name': parameter_types.name
    },
    'minProperties': 1,
    'additionalProperties': True
}
