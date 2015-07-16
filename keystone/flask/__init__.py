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

import functools
import os.path

import flask
import pbr.version

from keystone import config
from keystone import controllers
from keystone.server import common

from keystone.flask.blueprints import hello


def create_admin_app(global_conf):
    app = flask.Flask('keystone')

    from keystone.flask.blueprints import hello

    app.register_blueprint(hello.blueprint)

    return app


def create_main_app(global_conf):
    app = flask.Flask('keystone')

    from keystone.flask.blueprints import hello

    app.register_blueprint(hello.blueprint)

    return app


def fail_gracefully(f):
    """Logs exceptions and aborts."""
    @functools.wraps(f)
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            raise
            LOG.debug(e, exc_info=True)

            # exception message is printed to all logs
            LOG.critical(e)
            sys.exit(1)

    return wrapper


@fail_gracefully
def public_app_factory(global_conf, **local_conf):
    controllers.register_version('v2.0')
    app = flask.Flask('keystone:public')
    app.register_blueprint(hello.blueprint)
    return app


@fail_gracefully
def admin_app_factory(global_conf, **local_conf):
    controllers.register_version('v2.0')
    app = flask.Flask('keystone:admin')
    app.register_blueprint(hello.blueprint)
    return app


@fail_gracefully
def public_version_app_factory(global_conf, **local_conf):
    controllers.register_version('v2.0')
    app = flask.Flask('keystone:public:version')
    app.register_blueprint(hello.blueprint)
    return app


@fail_gracefully
def admin_version_app_factory(global_conf, **local_conf):
    app = flask.Flask('keystone:admin:version')
    app.register_blueprint(hello.blueprint)
    return app


@fail_gracefully
def v3_app_factory(global_conf, **local_conf):
    controllers.register_version('v3')
    app = flask.Flask('keystone:v3')
    app.register_blueprint(hello.blueprint)
    return app
