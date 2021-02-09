# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from flask.helpers import get_env
from flask_cors import CORS

from fm_database.models.user import User

from fm_frontend import api, auth, commands, public, user
from fm_frontend.extensions import cache, csrf_protect, db, debug_toolbar, login_manager, jwt, flask_manage_webpack


def create_app(config=None, testing=False, cli=False):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    
    configure_app(app, config, testing)
    register_extensions(app, cli)
    register_blueprints(app)
    register_errorhandlers(app)
    if cli:
        register_shellcontext(app)
        register_commands(app)

    return app


def configure_app(app, config=None, testing=False):
    """Set configuration for application."""

    if config:
        app.config.from_object(config)
        return

    # default configuration
    app.config.from_object('fm_frontend.settings.DevConfig')

    if testing is True:
        # override with testing config
        app.config.from_object('fm_frontend.settings.TestConfig')
    elif get_env() == 'production':
        # override with production config
        app.config.from_object('fm_frontend.settings.ProdConfig')


def register_extensions(app, cli):
    """Register Flask extensions."""
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    jwt.init_app(app)
    flask_manage_webpack.init_app(app)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)

    # api blueprints
    CORS(auth.views.blueprint)
    CORS(api.views.blueprint)
    csrf_protect.exempt(auth.views.blueprint)
    csrf_protect.exempt(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)

    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code), error=error), error_code
    for errcode in [400, 401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.init)
