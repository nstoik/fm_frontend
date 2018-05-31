# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect

from fm_database.extensions import pwd_context
from fm_database.models.base import get_base

pwd_context = pwd_context
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy(model_class=get_base())
cache = Cache()
debug_toolbar = DebugToolbarExtension()
webpack = Webpack()
