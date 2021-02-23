# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, jsonify, render_template
from flask.helpers import get_env
from flask_cors import CORS  # type: ignore
from fm_database.models.user import User

from fm_frontend import api, auth, public, user
from fm_frontend.extensions import (
    cache,
    csrf_protect,
    debug_toolbar,
    flask_static_digest,
    jwt,
    login_manager,
    smorest_api,
)


def create_app(config=None, testing=False):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])

    configure_app(app, config, testing)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)

    return app


def configure_app(app, config=None, testing=False):
    """Set configuration for application."""

    if config:
        app.config.from_object(config)
        return

    # default configuration
    app.config.from_object("fm_frontend.settings.DevConfig")

    if testing is True:
        # override with testing config
        app.config.from_object("fm_frontend.settings.TestConfig")
    elif get_env() == "production":
        # override with production config
        app.config.from_object("fm_frontend.settings.ProdConfig")


def register_extensions(app):
    """Register Flask extensions."""
    smorest_api.init_app(app)
    cache.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    jwt.init_app(app)
    flask_static_digest.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(api.user.views.blueprint)

    CORS(auth.views.blueprint)
    csrf_protect.exempt(auth.views.blueprint)
    app.register_blueprint(auth.views.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        # Try and get any data from the error.
        data = getattr(error, "data", None)
        if data is not None:
            # If there is data in the data field of the error,
            # the error came from the API. Render the error as follows
            return jsonify(data), error_code

        # Return the render_template of the error
        return render_template(f"{error_code}.html", error=error), error_code

    for errcode in [400, 401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"User": User}

    app.shell_context_processor(shell_context)
