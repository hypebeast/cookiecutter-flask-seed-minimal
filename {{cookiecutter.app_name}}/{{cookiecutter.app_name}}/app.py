# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template

from {{ cookiecutter.app_name }}.assets import assets
from {{ cookiecutter.app_name }}.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, migrate
from {{ cookiecutter.app_name }}.public import blueprint as public
from {{ cookiecutter.app_name }}.settings import Config, ProdConfig
from {{ cookiecutter.app_name }}.utils import pretty_date  # noqa

DEFAULT_BLUEPRINTS = (
    public,
)


def create_app(config_object=ProdConfig, app_name=None, blueprints=None):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    if app_name is None:
        app_name = Config.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)
    configure_app(app, config_object)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    return app


def configure_app(app, config_object):
    """Configure the flask app."""
    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(config_object)

    # http://flask.pocoo.org/docs/config/#instance-folders
    # app.config.from_pyfile('production.cfg', silent=True)


def configure_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def configure_blueprints(app, blueprints):
    """Register Flask blueprints."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_error_handlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def configure_hook(app):
    """Configure hook."""
    @app.before_request
    def before_request():
        pass


def configure_logging(app):
    """Configure logging."""
    loggers = [app.logger]
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    for logger in loggers:
        logger.setLevel(app.config['LOG_LEVEL'])
        logger.addHandler(stream_handler)


def configure_template_filters(app):
    """Configure template filters."""
    @app.template_filter()  # noqa
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)
