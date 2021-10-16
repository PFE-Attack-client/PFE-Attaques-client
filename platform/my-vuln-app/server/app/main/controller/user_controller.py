from flask import request
from flask_restx import Namespace, fields, Resource

api = Namespace('user', description='user related operations')
user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

@api.route('/')
@api.doc(params={'id': 'An ID'})
class UserList(Resource):
    def get(self):
        """List all registered users"""
        return True

    @api.response(201, 'User successfully created.')
    def post(self):
        """Creates a new User """
        data = request.json
        return data