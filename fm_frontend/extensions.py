# -*- coding: utf-8 -*-
"""Extensions module.

Each extension is initialized in the app factory located
in app.py.
"""
from flask_caching import Cache  # type: ignore
from flask_debugtoolbar import DebugToolbarExtension  # type: ignore
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow  # type: ignore
from flask_static_digest import FlaskStaticDigest  # type: ignore
from flask_wtf.csrf import CSRFProtect
from fm_database.extensions import pwd_context as fm_database_pwd_context

pwd_context = fm_database_pwd_context
csrf_protect = CSRFProtect()
login_manager = LoginManager()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
jwt = JWTManager()
ma = Marshmallow()
