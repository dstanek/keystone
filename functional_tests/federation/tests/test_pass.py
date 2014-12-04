# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

import testtools
from keystoneclient.v2_0 import client
from lxml import html
import requests
import six
from six.moves import urllib


LOG = logging.getLogger(__name__)


class Form(object):
    """Helper for parsing and POSTing forms."""

    def __init__(self, action=None, data=None):
        self.action = action
        self.data = data or {}

    @classmethod
    def from_response(cls, resp):
        root = html.document_fromstring(resp.content)

        form_node = root.xpath('//form')[0]
        action = form_node.get('action')
        if not action.startswith('http://'):
            action = urllib.parse.urljoin(resp.url, action)

        data = {}
        for el in root.xpath('//input'):
            data[el.get('name')] = el.get('value')

        return cls(action=action, data=data)

    def post(self):
        return requests.post(self.action, data=self.data)


class BasicTest(testtools.TestCase):
    USERNAME = 'haho0032'
    PASSWORD = 'qwerty'
    AUTH_URL = ('http://localhost:5000/v3/OS-FEDERATION/identity_providers/' +
                'pysaml2-idp/protocols/saml2/auth')

    def test(self):

        # Go to Federation auth on Keystone - we'll be ll be redirected
        # to the IdP's login page
        print 'GETting', AUTH_URL
        resp = requests.get(AUTH_URL)
        print 'Landed on', resp.url
        print

        # Parse the login form and pill it out so we can login
        form = Form.from_response(resp)
        form.data['login'] = USERNAME
        form.data['password'] = PASSWORD
        resp = form.post()
        print 'Landed on', resp.url
        print

        # Once you successfully login you get a crazy form that effectively
        # redirects you back to Keystone with signed SAML data.
        form = Form.from_response(resp)
        resp = form.post()
        print 'Landed on', resp.url
        print

        # The POST back to Keystone fails because mappings are not correct
        print resp.status_code
        print resp.headers
        print resp.content
