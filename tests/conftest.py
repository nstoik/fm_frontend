"""Defines fixtures available to all tests."""
# pylint: disable=redefined-outer-name

import json

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fm_database.base import create_all_tables, drop_all_tables, get_session
from fm_database.models.user import User
from webtest import TestApp

from fm_frontend.app import create_app
from fm_frontend.settings import TestConfig

from .factories import UserFactory


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


@pytest.fixture(scope="session")
def dbsession():
    """Returns an sqlalchemy session."""

    yield get_session()


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture
def tables(dbsession):
    """Create all tables for testing. Delete when done."""
    create_all_tables()
    yield
    dbsession.close()
    drop_all_tables()


@pytest.fixture
def user(dbsession):
    """A user for the tests."""
    user = UserFactory.create(session=dbsession, password="myprecious")
    dbsession.commit()
    return user


@pytest.fixture
def admin_user(dbsession):
    """An admin user for the tests."""
    user = User(username="admin", email="admin@admin.com", password="admin")

    dbsession.add(user)
    dbsession.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    """Log in the admin user and get the access_token."""
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }
