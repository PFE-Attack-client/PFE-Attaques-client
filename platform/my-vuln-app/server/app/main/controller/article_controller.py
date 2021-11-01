from flask import request
from flask_restx import Namespace, fields, Resource

api = Namespace('article', description='Article related operations')
user = api.model('article', {
        'title': fields.String(required=True, description='article title'),
        'author': fields.String(required=True, description='article author'),
        'article_img': fields.String(required=True, description='article img link'),
        'date': fields.String(description='article publication date')
    })

@api.route('/')
@api.doc()
class ArticleList(Resource):
    def get(self):
        pass

@api.route('/comment')
class ArticleComment(Resource):
    def get():
        pass

    def post():
        pass
