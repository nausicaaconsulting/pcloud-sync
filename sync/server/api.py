import logging
import functools

from sync.auth import api_auth_secret_code

from flask import Blueprint, request
from flask_restx import Api, fields, Resource, Namespace
from werkzeug.exceptions import Unauthorized
from sqlalchemy import func, or_, and_

logger = logging.getLogger(__name__)


def is_call_authenticated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (
                'X-Simple-Authentication' in request.headers
                and request.headers['X-Simple-Authentication'] == api_auth_secret_code()
        ):
            return func(*args, **kwargs)
        raise Unauthorized()
    return wrapper


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

config_namespace = Namespace('Config', path='/config', decorators=[is_call_authenticated])

api = Api(api_blueprint)

api.add_namespace(config_namespace)

@config_namespace.route('/')
class TestResource(Resource):
    def get(self):
        return {}, 200
