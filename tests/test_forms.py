# -*- coding: utf-8 -*-
"""Test forms."""
# pylint: disable=unused-argument
import pytest

from fm_frontend.public.forms import LoginForm
from fm_frontend.user.forms import RegisterForm

@pytest.mark.usefixtures("app")
class TestRegisterForm:
    """Register form."""

    @staticmethod
    def test_validate_user_already_registered(user):
        """Enter username that is already registered."""
        form = RegisterForm(
            username=user.username,
            email="foo@bar.com",
            password="example",
            confirm="example",
        )

        assert form.validate() is False
        assert "Username already registered" in form.username.errors

    @staticmethod
    def test_validate_email_already_registered(user):
        """Enter email that is already registered."""
        form = RegisterForm(
            username="unique", email=user.email, password="example", confirm="example"
        )

        assert form.validate() is False
        assert "Email already registered" in form.email.errors

    @staticmethod
    def test_validate_success(tables):
        """Register with success."""
        form = RegisterForm(
            username="newusername",
            email="new@test.test",
            password="example",
            confirm="example",
        )
        assert form.validate() is True

@pytest.mark.usefixtures("app")
class TestLoginForm:
    """Login form."""

    @staticmethod
    def test_validate_success(user, dbsession):
        """Login successful."""
        user.set_password("example")
        user.save(dbsession)
        form = LoginForm(username=user.username, password="example")
        assert form.validate() is True
        assert form.user.id == user.id

    @staticmethod
    def test_validate_unknown_username(tables):
        """Unknown username."""
        form = LoginForm(username="unknown", password="example")
        assert form.validate() is False
        assert "Unknown username" in form.username.errors
        assert form.user is None

    @staticmethod
    def test_validate_invalid_password(user, dbsession):
        """Invalid password."""
        user.set_password("example")
        user.save(dbsession)
        form = LoginForm(username=user.username, password="wrongpassword")
        assert form.validate() is False
        assert "Invalid password" in form.password.errors

    @staticmethod
    def test_validate_inactive_user(user, dbsession):
        """Inactive user."""
        user.active = False
        user.set_password("example")
        user.save(dbsession)
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password="example")
        assert form.validate() is False
        assert "User not activated" in form.username.errors
