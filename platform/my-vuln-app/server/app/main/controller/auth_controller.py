from flask import request
from flask_restx import Namespace, fields, Resource
from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..service.auth_service import Auth
api = Namespace('auth', description='Login/logout from the API')
user_auth = api.model('auth_details', 
{
    'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password ')
})

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)

@api.route('/logout')
class Userlogout(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
