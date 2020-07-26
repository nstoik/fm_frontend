from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from marshmallow import fields

from fm_database.models.user import User, Role

from fm_frontend.extensions import ma, db
from fm_frontend.commons.pagination import paginate


class UserSchema(ma.ModelSchema):

    # password = ma.String(load_only=True, required=True)

    class Meta:
        exclude = ["password",]
        model = User
        sqla_session = db.session


class RoleSchema(ma.ModelSchema):

    class Meta:
        model = Role
        sqla_session = db.session


class UserResource(Resource):
    """Single object resource
    """
    method_decorators = [jwt_required]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        try:
            user = schema.load(request.json, instance=user)
        except ValidationError as err:
            return err.normalized_messages(), 422

        user.save(db.session)

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        user.delete(db.session)

        return {"msg": "user deleted"}


class UserList(Resource):
    """Creation and get_all
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        try:
            user = schema.load(request.json)
        except ValidationError as err:
            return err.normalized_messages(), 422

        user.save(db.session)

        return {"msg": "user created", "user": schema.dump(user)}, 201


class RoleResource(Resource):
    """Single object resource
    """
    method_decorators = [jwt_required]

    def get(self, role_id):
        schema = RoleSchema()
        role = Role.query.get_or_404(role_id)
        return {"role": schema.dump(role)}

    def put(self, role_id):
        schema = RoleSchema(partial=True)
        role = Role.query.get_or_404(role_id)
        try:
            role = schema.load(request.json, instance=role)
        except ValidationError as err:
            return err.normalized_messages(), 422

        role.save(db.session)

        return {"msg": "role updated", "role": schema.dump(role)}

    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        role.delete(db.session)

        return {"msg": "role deleted"}


class RoleList(Resource):
    """Creation and get_all
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = RoleSchema(many=True)
        query = Role.query
        return paginate(query, schema)

    def post(self):
        schema = RoleSchema()
        try:
            role = schema.load(request.json)
        except ValidationError as err:
            return err.normalized_messages(), 422

        role.save(db.session)

        return {"msg": "role created", "role": schema.dump(role)}, 201