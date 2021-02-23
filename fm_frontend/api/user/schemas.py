"""Schema for User and Roles."""
from fm_database.base import get_session
from fm_database.models.user import Role, User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow UserSchema that loads the instance."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for UserSchema."""

        exclude = ("password",)

        sqla_session = get_session()
        model = User
        include_relationships = True
        load_instance = True


class UserSchemaDict(SQLAlchemyAutoSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow UserSchema that produces a dict of changed values."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for UserSchema."""

        exclude = ("password",)

        sqla_session = get_session()
        model = User
        include_relationships = True


class RoleSchema(SQLAlchemyAutoSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow RoleSchema."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for RoleSchema."""

        sqla_session = get_session()
        model = Role
        include_relationships = True
        load_instance = True
