from flask import request
from flask_restx import Resource, abort

from webapp.api.auth.login_view import credentialsRequestParser
from webapp.extensions import db, api_
from webapp.models import User


@api_.expect(credentialsRequestParser)
class RegisterView(Resource):
    @api_.response(201, '')
    @api_.response(400, '&lt;Error description&gt;')
    def post(self):
        content: dict = request.json

        username = content.get("username", None)
        password = content.get("password", None)

        if not username:
            abort(400, "Username field is missing or empty.")
        elif not password:
            abort(400, "Password field is missing or empty.")

        # Check if username is already taken
        user = User.query.filter(User.username == username).first()
        if user is not None:
            abort(400, "Username is already taken.")

        # Create new user
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {}, 201
