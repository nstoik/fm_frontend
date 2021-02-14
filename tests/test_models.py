# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest
from fm_database.base import get_session
from fm_database.models.user import Role, User

from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, db):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save(db.session)

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self, db):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save(db.session)
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self, db):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save(db.session)
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self, db):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123', session=db.session)
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self, db):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save(db.session)
        user = UserFactory()
        user.roles.append(role)
        user.save(db.session)
        assert role in user.roles
