from flask import (
    Flask,
    session,
    jsonify,
    url_for,
    redirect,
    render_template,
    make_response,
)
from flask_restx import Api, Resource
from flaskr.db import db
from flaskr.models import User
from flask_sqlalchemy import session as sql_session
from sqlalchemy import insert, select
from flaskr.apis import api
from flaskr.blueprints import bp_google_auth
import logging
import sys
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .rate_limiter import limiter
from flask_talisman import Talisman


app = Flask(__name__)
app.config.from_object("flaskr.settings")

# jwt
jwt = JWTManager(app)
# bcrypt
bcrypt = Bcrypt(app)
oauth = OAuth(app)

# cors
CORS(app)

# authlib logging
log = logging.getLogger("authlib")
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

# HTTP security headers for Flask
# Forces all connects to https, unless running with debug enabled
# CSP set to none for now, for testing purposes
Talisman(app, content_security_policy=None, force_https=False)

# cors logger
logging.getLogger("flask_cors").level = logging.DEBUG

oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=app.config['GOOGLE_SERVER_METADATA_URL'],
    client_kwargs={"scope": "openid email profile"},
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
)

# limiter
limiter.init_app(app)

# initialize the app with the database extension
db.init_app(app)

# add the api to the app
api.init_app(app)

# add the google auth blueprint to the app
app.register_blueprint(bp_google_auth)

# update app config objects
app.config.update(
    {
        "oauth": oauth,
    }
)


# create the table schema in the database
""" with app.app_context():

    db.drop_all()
    db.create_all()

    # create users
    db.session.execute(
        insert(User),
        [
            {
                "id": 1,
                "username": "spongebob",
                "fullname": "Spongebob Squarepants",
                "email": "spongebob@gmail.com",
                "password": bcrypt.generate_password_hash("xx5xxx").decode("utf-8"),
            },
            {
                "id": 2,
                "username": "sandy",
                "fullname": "Sandy Cheeks",
                "email": "sandycheeks@gmail.com",
                "password": bcrypt.generate_password_hash("yyy4yy").decode("utf-8"),
            },
            {
                "id": 3,
                "username": "patrick",
                "fullname": "Patrick Star",
                "email": "patrickstar@gmail.com",
                "password": bcrypt.generate_password_hash("jjj7jj").decode("utf-8"),
            },
            {
                "id": 4,
                "username": "squidward",
                "fullname": "Squidward Tentacles",
                "email": "squidwardtentacles@gmail.com",
                "password": bcrypt.generate_password_hash("tt4ttt").decode("utf-8"),
            },
            {
                "id": 5,
                "username": "ehkrabs",
                "fullname": "Eugene H. Krabs",
                "email": "eugeneKrabs@gmail.com",
                "password": bcrypt.generate_password_hash("mmm2mmm").decode("utf-8"),
            },
        ],
    )
    db.session.commit() """


if __name__ == "__main__":
    app.run(debug=True)
