"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name, unused-argument

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import url_for
from flask.testing import FlaskClient
from fm_database.base import create_all_tables, drop_all_tables, get_session
from fm_database.models.user import User
from webtest import TestApp

from fm_frontend.app import create_app
from fm_frontend.settings import TestConfig

from .factories import UserFactory


class HtmlTestClient(FlaskClient):
    """Override the FlaskClient with some login and logout methods."""

    def login_user(self, username="user0", password="myprecious"):
        """Login a user that is created from the UserFactory."""
        return self.login_with_creds(username, password)

    def login_with_creds(self, username, password):
        """Send the login data to the login url."""
        return self.post(
            url_for("public.home"), data=dict(username=username, password=password)
        )

    def logout(self):
        """Logout."""
        self.get("public.logout")


@pytest.fixture(scope="session")
# pylint: disable=unused-argument
def monkeysession(request):
    """Create a MonkeyPatch object that can be scoped to a session.

    https://github.com/pytest-dev/pytest/issues/363#issuecomment-289830794
    """
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session", autouse=True)
# pylint: disable=unused-argument
def set_testing_env(monkeysession, database_env):
    """Set the environment variable for testing.

    This executes once for the entire session of testing.
    The environment variables are set back to the default after.
    Makes sure that the database env is also called and set.
    """
    monkeysession.setenv("FM_FRONTEND_CONFIG", "test")
    yield
    monkeysession.setenv("FM_FRONTEND_CONFIG", "dev")


@pytest.fixture(scope="session")
def database_env(monkeysession):
    """Set the fm_database env variable for testing and set back when done.."""
    monkeysession.setenv("FM_DATABASE_CONFIG", "test")
    yield
    monkeysession.setenv("FM_DATABASE_CONFIG", "dev")


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def flaskclient(app):
    """Create a flask test client for tests. Alternative to testapp that supports logging a user in."""
    app.test_client_class = HtmlTestClient
    with app.test_client() as client:
        yield client


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture(scope="session")
def dbsession():
    """Returns an sqlalchemy session."""
    yield get_session()


@pytest.fixture
def tables(dbsession):
    """Create all tables for testing. Delete when done."""
    create_all_tables()
    yield
    dbsession.close()
    drop_all_tables()


@pytest.fixture
def user(dbsession, tables):
    """A user for the tests."""
    user = UserFactory.create(session=dbsession, password="myprecious")
    dbsession.commit()
    return user


@pytest.fixture
def admin_user(dbsession, tables):
    """An admin user for the tests."""
    user = User(username="admin", email="admin@admin.com", password="admin")
    user.is_admin = True

    dbsession.add(user)
    dbsession.commit()

    return user


@pytest.fixture
def auth_headers(admin_user, flaskclient, tables):
    """Log in the admin user and get an access_token."""
    data = {"username": admin_user.username, "password": "admin"}
    rep = flaskclient.post(
        "/auth/login",
        json=data,
        headers={"content-type": "application/json"},
    )
    tokens = rep.get_json()
    return {
        "content-type": "application/json",
        "authorization": f"Bearer { tokens['access_token'] }",
    }
