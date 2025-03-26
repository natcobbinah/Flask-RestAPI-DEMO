from flask import Flask, session, jsonify, url_for, redirect, render_template
from flask_restx import Api, Resource
from flaskr.db import db
from flaskr.models import User
from flask_sqlalchemy import session as sql_session
from sqlalchemy import insert, select
from flaskr.apis import api
import logging
import sys
from authlib.integrations.flask_client import OAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object("flaskr.settings")

# jwt
jwt = JWTManager(app)
# bcrypt
bcrypt = Bcrypt(app)
oauth = OAuth(app)

#redirect url = http://127.0.0.1:5000/callback/google

# logging
log = logging.getLogger("authlib")
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
)


# initialize the app with the database extension
db.init_app(app)

# add the api to the app
api.init_app(app)


@app.route('/home')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    print(token)
    session['user'] = token['userinfo']
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/home')

#create the table schema in the database
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
