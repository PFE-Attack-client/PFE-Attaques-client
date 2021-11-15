from flask import request
from flask_restx import Namespace, fields, Resource
from ..service.user_service import save_new_user, get_all_users, get_a_user

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


@api.route('/signup')
class UserSignup(Resource):
    @api.marshal_list_with(user, envelope='data')
    def get(self):
        pass
    
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(user, validate=True)
    def post(self):
        """Register a User in the database"""
        data = request.json
        print(request)
        return save_new_user(data=data)