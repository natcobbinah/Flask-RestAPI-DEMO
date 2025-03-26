from flask_restx import Namespace, Resource, fields
from flask import jsonify
from flask_restx import Api, Resource
from flaskr.db import db
from flaskr.models import User
from flask_sqlalchemy import session
from sqlalchemy import insert, select, and_
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_bcrypt import generate_password_hash, check_password_hash

authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}

api = Namespace(
    "users",
    description="User related operations",
    authorizations=authorizations,
)


user_model_desc = api.model(
    "User",
    {
        "id": fields.Integer(required=True, description="The user identifier"),
        "username": fields.String(required=True, description="The user name"),
        "fullname": fields.String(required=True, description="The user fullname"),
        "email": fields.String(required=True, description="The users email"),
        "password": fields.String(required=True, description="The users password"),
    },
)

create_user_parser = api.parser()
create_user_parser.add_argument("username", type=str, location="form")
create_user_parser.add_argument("fullname", type=str, location="form")
create_user_parser.add_argument("email", type=str, location="form")
create_user_parser.add_argument("password", type=str, location="form")
create_user_parser.add_argument("verify password", type=str, location="form")

login_user_parser = api.parser()
login_user_parser.add_argument("email", type=str, location="form")
login_user_parser.add_argument("password", type=str, location="form")


authorization_header_parser = api.parser()
authorization_header_parser.add_argument(
    "Authorization", location="headers", type=str, required=True
)


@api.route("/users")
class UsersList(Resource):

    @api.doc("list_users")
    @api.doc(security=None)
    def get(self):
        stmt = select(User).order_by(User.id)
        users = db.session.execute(stmt).scalars().all()
        user_records = [
            {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "email": user.email,
            }
            for user in users
        ]
        return jsonify({"users": user_records})

    @api.doc("create_user")
    @api.doc(security=None)
    @api.expect(create_user_parser)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username")
        fullname = args.get("fullname")
        email = args.get("email")
        password = args.get("password")
        verify_password = args.get("verify password")

        if password != verify_password:
            return jsonify({"message": "Passwords do not match"})

        users_count = db.session.query(User).count()

        user = User(
            id=users_count + 1,
            username=username,
            fullname=fullname,
            email=email,
            password=generate_password_hash(password).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User account created successfully"})


@api.route("/access")
class UserLogin(Resource):

    @api.doc(security="Bearer")
    @jwt_required()
    #@api.expect(authorization_header_parser)
    def get(self):
        current_user = get_jwt_identity()
        return jsonify({"logged_in_as": current_user})

    @api.doc("login")
    @api.expect(login_user_parser)
    @api.doc(security=None)
    def post(self):
        args = login_user_parser.parse_args()
        email = args.get("email")
        password = args.get("password")

        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar()

        if user is None:
            return jsonify({"message": "User not found"})

        # compare hash of user record retrieved password to user_input password
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({"username": user.username, "access_token": access_token})
        else:
            return jsonify({"message": "Password is incorrect"})
    
            

        
