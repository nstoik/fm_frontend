"""Authorization views."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from fm_database.models.user import User

from fm_frontend.extensions import jwt

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
def login():
    """Authenticate user and return token."""
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 400

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    return jsonify(ret), 200


@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Return an updated access_token using a refresh_token."""
    current_user = get_jwt_identity()
    ret = {"access_token": create_access_token(identity=current_user)}
    return jsonify(ret), 200


@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, jwt_data):
    """Load the user given JWT.

    A callback function that loades a user from the database whenever
    a protected route is accessed. This returns a User or else None
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.user_identity_loader
def user_identity_lookup(user):
    """Return the user identity.

    A callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id
