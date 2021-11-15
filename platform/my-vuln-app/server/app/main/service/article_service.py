import datetime
from app.main import db
from app.main.model.article import Article, Commentary, ArticleSchemas, CommentarySchemas

def save_new_commentary(id, data):
    article = Article.query.filter_by(id=id).first()
    if article:
        new_commentary = Commentary(
            title=data['title'],
            author=data['author'],
            date=datetime.datetime.utcnow(),
            content= data['content'],
            article_id = id
        )
        save_changes(new_commentary)
        response_object = {
            'status' : 'success',
            'message' : 'Your commentary has been saved.'
        }
        return response_object, 201
    else:
        response_object = {
            'status' : 'fail', 
            'message' : 'the article does not exist'
        }
        return response_object, 409

def get_all_articles():
    articles = Article.query.all()
    article_schemas = ArticleSchemas(many=True)
    res = article_schemas.dump(articles)
    return {'articles': res}
    
def get_all_commentaries(id):
    article = Article.query.filter_by(id=id).first()
    if article:
        commentaries = Commentary.query.filter_by(article_id=id)
        com_schema = CommentarySchemas(many=True)
        res = com_schema.dump(commentaries)
        return {'commentaries': res}
    else:
        response_object = {
            'status' : 'fail', 
            'message' : 'the article does not exist'
        }
    return response_object, 409

def save_changes(data):
    db.session.add(data)
    db.session.commit()