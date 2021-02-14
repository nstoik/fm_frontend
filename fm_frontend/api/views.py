from flask import Blueprint
from flask_restful import Api

from fm_frontend.api.resources import RoleList, RoleResource, UserList, UserResource

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(RoleResource, '/roles/<int:role_id>')
api.add_resource(RoleList, '/roles')
