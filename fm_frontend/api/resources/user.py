from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

from fm_database.models.user import User

from fm_frontend.extensions import ma, db
from fm_frontend.commons.pagination import paginate


class UserSchema(ma.ModelSchema):

    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
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

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

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

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user)}, 201
