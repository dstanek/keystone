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
"""Common parameter types for validating a request reference."""

from keystone import config

import jsd


CONF = config.CONF


Object = jsd.Object
Boolean = jsd.Boolean

boolean = {
    'type': 'boolean',
    'enum': [True, False]
}

# NOTE(lbragstad): Be mindful of this pattern as it might require changes
# once this is used on user names, LDAP-based user names specifically since
# commas aren't allowed in the following pattern. Here we are only going to
# check the length of the name and ensure that it's a string. Right now we are
# not going to validate on a naming pattern for issues with
# internationalization.
name = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 255
}

def Name(required=False):
    return jsd.String(min_len=1, max_len=255, required=required)


class IdString(jsd.String):
    type = 'string'
    min_len = 1
    max_len = 64

    @property
    def pattern(self):
        # NOTE(dstanek): this is a property so that it can be evaluated
        # lazily. This can't be executed at import time because the
        # config options wouldn't have been setup.
        return CONF.validation.id_string_regex


required_id_string = {
    'type': 'string',
    'minLength': 1,
    'maxLength': 64,
    #'pattern': CONF.validation.id_string_regex
    'pattern': '^[a-zA-Z0-9-]+$',
}

optional_id_string = {
    'type': ['string', 'null'],
    'minLength': 1,
    'maxLength': 64,
    #'pattern': CONF.validation.id_string_regex
    'pattern': '^[a-zA-Z0-9-]+$',
}

Description = jsd.String

description = {
    'type': ['string', 'null']
}


class Url(jsd.String):
    type = 'string'
    min_len = 0
    max_len = 225
    pattern = ('^https?://'
               '(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'
               '+[a-zA-Z]{2,6}\.?|'
               'localhost|'
               '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
               '(?::\d+)?'
               '(?:/?|[/?]\S+)$')

url = {
    'type': 'string',
    'minLength': 0,
    'maxLength': 225,
    # NOTE(lbragstad): Using a regular expression here instead of the
    # FormatChecker object that is built into jsonschema. The FormatChecker
    # can validate URI formats but it depends on rfc3987 to do that
    # validation, and rfc3987 is GPL licensed. For our purposes here we will
    # use a regex and not rely on rfc3987 to validate URIs.
    'pattern': '^https?://'
               '(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'
               '+[a-zA-Z]{2,6}\.?|'
               'localhost|'
               '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
               '(?::\d+)?'
               '(?:/?|[/?]\S+)$'
}

Email = jsd.Email

email = {
    'type': 'string',
    'format': 'email'
}
