# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os.path
import socket
import sys
from wsgiref import simple_server

from oslo_config import cfg
import oslo_i18n
import pbr.version


# NOTE(dstanek): i18n.enable_lazy() must be called before
# keystone.i18n._() is called to ensure it has the desired lazy lookup
# behavior. This includes cases, like keystone.exceptions, where
# keystone.i18n._() is called at import time.
oslo_i18n.enable_lazy()


# If ../../keystone/__init__.py exists, add ../../ to Python search path, so
# that it will override what happens to be installed in
# /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                   os.pardir,
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'keystone', '__init__.py')):
    sys.path.insert(0, possible_topdir)


from keystone import config
from keystone import flask
from keystone.openstack.common import service
from keystone.server import common
from keystone import service as keystone_service


class ServerAdapter(object):
    """Adapts a WSGIServer instance to the interface required by launcher.
    """

    def __init__(self, name, server):
        self._name = name
        self._server = server

    def start(self):
        hostname = socket.gethostbyname(self._server.server_name)
        port = self._server.server_port
        print('Serving %s on %s:%s' % (self._name, hostname, port))

        self._server.serve_forever()


def serve(*servers):
    launcher = service.ProcessLauncher()
    for name, server in servers:
        try:
            launcher.launch_service(server, 1)
        except socket.error:
            logging.exception(_('Failed to start the %(name)s server'),
                {'name': name})
            raise

    for name, server in servers:
        launcher.wait()


def keystone_setup():
    dev_conf = os.path.join(possible_topdir, 'etc', 'keystone.conf')
    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]

    common.configure(
        version=pbr.version.VersionInfo('keystone').version_string(),
        config_files=config_files)


def main():
    #from keystone.flask import apps

    keystone_setup()

    paste_config = config.find_paste_config()

    admin_server = simple_server.make_server(
        cfg.CONF.eventlet_server.admin_bind_host,
        cfg.CONF.eventlet_server.admin_port,
        keystone_service.loadapp('config:%s' % paste_config, 'public_version_service'))
        #apps.admin)
    public_server = simple_server.make_server(
        cfg.CONF.eventlet_server.public_bind_host,
        cfg.CONF.eventlet_server.public_port,
        keystone_service.loadapp('config:%s' % paste_config, 'public_version_service'))
        #apps.public)
    serve(('admin', ServerAdapter('admin', admin_server)),
          ('public', ServerAdapter('public', public_server)))
