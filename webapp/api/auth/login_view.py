from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Resource, abort, fields

from webapp.extensions import api_
from webapp.models import User

credentialsRequestParser = api_.parser()
credentialsRequestParser.add_argument('username', type=str, help='Username for logging in.', location='json',
                                      required=True)
credentialsRequestParser.add_argument('password', type=str, help='Password for logging in.', location='json',
                                      required=True)


loginData = api_.model('loginData', {
    "access_token": fields.String(description='A token to access protected resources on the server.')
})


@api_.expect(credentialsRequestParser)
class LoginView(Resource):
    @api_.marshal_with(loginData, code=200, description="Get access token")
    @api_.response(400, '&lt;Error description&gt;')
    @api_.response(401, 'Invalid credentials')
    def post(self):
        content: dict = request.json
        if content is None:
            abort(400, "Missing username and password.")

        username = content.get("username", None)
        password = content.get("password", None)

        if not username:
            abort(400, "Username field is missing or empty.")
        elif not password:
            abort(400, "Password field is missing or empty.")

        # Check if user exists and check password
        user: User = User.query.filter(User.username == username).first()
        if (user is None) or (not user.check_password(password)):
            abort(401, 'Invalid credentials')

        # Create JWT token
        access_token = create_access_token(
            identity=user.get_jwt_content(),
            # Prevents JWT tokens from expiring
            expires_delta=False)

        return {"access_token": access_token}, 200
