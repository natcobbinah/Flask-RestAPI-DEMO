# myapp/settings.py

from environs import Env

env = Env()
env.read_env()

# Override in .env for local development
DEBUG = env.bool("FLASK_DEBUG", default=False)
# SECRET_KEY is required
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = env.str("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool(
    "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
)

# OAuth
GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET")
# GOOGLE_AUTHORIZE_URL=env.str("GOOGLE_AUTHORIZE_URL")
# GOOGLE_ACCESS_TOKEN_URL=env.str("GOOGLE_ACCESS_TOKEN_URL")

# JWT
JWT_SECRET_KEY = env.str("JWT_SECRET_KEY")
JWT_HEADER_TYPE = env.str("JWT_HEADER_TYPE", default="Bearer")
JWT_HEADER_NAME = env.str("JWT_HEADER_NAME", default="Authorization")
