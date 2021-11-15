from flask import request
from flask_restx import Namespace, fields, Resource
from ..service.article_service import save_new_commentary, get_all_articles, get_all_commentaries

api = Namespace('article', description='Article related operations')
article = api.model('article', {
        'title': fields.String(required=True, description='article title'),
        'author': fields.String(required=True, description='article author'),
        'article_img': fields.String(required=True, description='article img link'),
        'date': fields.String(description='article publication date')
    })

@api.route('/')
@api.doc()
class ArticleList(Resource):
    def get(self):
        return get_all_articles()

@api.route('/<id>/comment/')
class ArticleComment(Resource):
    def get(self, id):
        return get_all_commentaries(id)

    def post(self, id):
        data = request.json
        return save_new_commentary(id , data)
