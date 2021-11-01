from flask import Flask, Blueprint
from flask_restx import Api
from .main.controller.user_controller import api as user_ns
from .main.controller.article_controller import api as article_ns
from .main.controller.auth_controller import api as auth_ns
blueprint = Blueprint('api', __name__)

api = Api(blueprint,
        title='vuln-app-API',
        version='0',
        description='basic endpoits for a front-end / back-end application'
        )

api.add_namespace(user_ns, path='/user')
api.add_namespace(article_ns, path='/article')
api.add_namespace(auth_ns, path="/auth")