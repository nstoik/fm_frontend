"""User Resource."""
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from fm_database.base import get_session
from fm_database.models.user import Role, User
from marshmallow.exceptions import ValidationError

from fm_frontend.commons.pagination import paginate
from fm_frontend.extensions import ma


class UserSchema(
    ma.SQLAlchemySchema
):  # pylint: disable=too-many-ancestors,too-few-public-methods
    """Marshmallow UserSchema."""

    password = ma.String(load_only=True, required=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for UserSchema."""

        # exclude = ["password",]
        model = User
        sqla_session = get_session()


class RoleSchema(
    ma.SQLAlchemySchema
):  # pylint: disable=too-many-ancestors,too-few-public-methods
    """Marshmallow RoleSchema."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for RoleSchema."""

        model = Role
        sqla_session = get_session()


class UserResource(Resource):
    """Single object User resource."""

    method_decorators = [jwt_required]

    @staticmethod
    def get(user_id):
        """Get User schema."""
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    @staticmethod
    def put(user_id):
        """Update User."""
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        try:
            user = schema.load(request.json, instance=user)
        except ValidationError as err:
            return err.normalized_messages(), 422

        user.save(get_session())

        return {"msg": "user updated", "user": schema.dump(user)}

    @staticmethod
    def delete(user_id):
        """Delete User."""
        user = User.query.get_or_404(user_id)
        user.delete(get_session())

        return {"msg": "user deleted"}


class UserList(Resource):
    """Multi object User resource."""

    method_decorators = [jwt_required]

    @staticmethod
    def get():
        """Get User List."""
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    @staticmethod
    def post():
        """Create User."""
        schema = UserSchema()
        try:
            user = schema.load(request.json)
        except ValidationError as err:
            return err.normalized_messages(), 422

        user.save(get_session())

        return {"msg": "user created", "user": schema.dump(user)}, 201


class RoleResource(Resource):
    """Single object Role resource."""

    method_decorators = [jwt_required]

    @staticmethod
    def get(role_id):
        """Get the Role object."""
        schema = RoleSchema()
        role = Role.query.get_or_404(role_id)
        return {"role": schema.dump(role)}

    @staticmethod
    def put(role_id):
        """Update the Role object."""
        schema = RoleSchema(partial=True)
        role = Role.query.get_or_404(role_id)
        try:
            role = schema.load(request.json, instance=role)
        except ValidationError as err:
            return err.normalized_messages(), 422

        role.save(get_session())

        return {"msg": "role updated", "role": schema.dump(role)}

    @staticmethod
    def delete(role_id):
        """Delete the Role object."""
        role = Role.query.get_or_404(role_id)
        role.delete(get_session())

        return {"msg": "role deleted"}


class RoleList(Resource):
    """Multi object Role resource."""

    method_decorators = [jwt_required]

    @staticmethod
    def get():
        """Get list of Role objects."""
        schema = RoleSchema(many=True)
        query = Role.query
        return paginate(query, schema)

    @staticmethod
    def post():
        """Create Role object."""
        schema = RoleSchema()
        try:
            role = schema.load(request.json)
        except ValidationError as err:
            return err.normalized_messages(), 422

        role.save(get_session())

        return {"msg": "role created", "role": schema.dump(role)}, 201
