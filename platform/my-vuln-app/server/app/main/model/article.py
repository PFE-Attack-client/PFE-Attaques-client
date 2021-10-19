from .. import db

class Article(db.Model):
    """ Article model for storing article related details """
    __tablename__ = "article"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(80))
    article_img = db.Column(db.String(100))
    content = db.Column(db.String(400))
    date = db.Column(db.DateTime, nullable=False)
    commentaries = db.relationship('Commentary', backref='article', lazy=True)
    
    def __repr__(self):
        return '<Article %r>' % self.title

class Commentary(db.Model):

    __tablename__ = "commentary"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(80))
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(400))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)

    def __repr__(self):
        return '<commentary %r>' % self.content