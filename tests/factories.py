# -*- coding: utf-8 -*-
"""Factories to help in tests."""
# pylint: disable=too-few-public-methods
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from fm_database.models.user import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    @classmethod
    def create(cls, session, **kwargs):
        """Override the create method of the SQLALchemyModelFactory class.

        Adds the variable session so that the sqlalchemy_session can be
        passed in and overwritten. The sqlalchemy_session is passed in this
        way so that the new object can be properly saved in the correct session.
        """
        cls._meta.sqlalchemy_session = session
        return super().create(**kwargs)

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = None


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = PostGenerationMethodCall("set_password", "example")
    active = True

    class Meta:
        """Factory configuration."""

        model = User
