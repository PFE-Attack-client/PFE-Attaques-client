from .. import db
from flask import Flask, request

from marshmallow import Schema, fields, ValidationError, pre_load


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

class ArticleSchemas(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    author = fields.Str()
    article_img = fields.Str()
    content = fields.Str()
    date = fields.DateTime(dump_only=True)

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
        
class CommentarySchemas(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    author = fields.Str()
    date = fields.DateTime(dump_only=True)
    content = fields.Str()
    article_id = fields.Int(dump_only=True)