#!/usr/bin/env python3
""" Module of Session Authentication views
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 401 if password is wrong
      - 404 if no user found for the email
    """
    email = request.form.get("email")

    if email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")

    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    user = users[0]

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
