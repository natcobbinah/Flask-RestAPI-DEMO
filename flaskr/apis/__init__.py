from flask_restx import Api
from .usernamespace import api as users_api


api = Api(
    title="TP Auth Demo",
    version="1.0",
    description="A demo application for TP Auth using OAuth2",
    # All API metadatas
)

api.add_namespace(users_api)
