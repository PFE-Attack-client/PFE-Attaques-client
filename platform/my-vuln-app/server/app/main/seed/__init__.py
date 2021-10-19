import sys 
import datetime
sys.path.append('..')
from flask import Flask
from app.main.model.article import Article, Commentary
from app.main.config.db import db_sqlAlchemy as db
from app.main.model.user import User

user1 = User(email="local@host.gouv", username="local", registered_on=datetime.datetime.utcnow(), password="kikou")
user2 = User(email="local2@host.gouv", username="local2", registered_on=datetime.datetime.utcnow(), password="kikou")

article1 = Article(
    title="how to hack your girlfriend's facebook account",
    author="Jean-article",
    date=datetime.datetime.utcnow(),
    content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcuIn enim justo, rhoncus ut, imperdiet a",
    article_img="notnow"
)

article2 = Article(
    title="how to hack your bank account to add unlimited money",
    author="Jean-article",
    date=datetime.datetime.utcnow(),
    content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu In enim justo, rhoncus ut, imperdiet a",
    article_img="notnow"
)

def seed_the_db():
    print("filling the database..")
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(article1)
    db.session.add(article2)
    db.session.commit()

def seed_commentaries():
    article1 = Article.query.filter_by(title="how to hack your girlfriend's facebook account").first()
    mean_commentary1 = Commentary(
        title = "Does it work with my boyfriend too?",
        author= "prefer not to say",
        date = datetime.datetime.utcnow(),
        content ="please answer me it is very important",
        article_id = article1.id
    )
    mean_commentary2 = Commentary(
        title = "thx man",
        author= "the future hacker",
        date = datetime.datetime.utcnow(),
        content ="man it's so crazy, I have stolen my sister account lol she is crying lol",
        article_id = article1.id
    )
    article2 = Article.query.filter_by(title="how to hack your bank account to add unlimited money").first()
    mean_commentary3 = Commentary(
        title = "why it does not work",
        author= "prefer not to say",
        date = datetime.datetime.utcnow(),
        content ="man you suck it is not working, i will have to go to school now",
        article_id = article2.id
    )
    mean_commentary4 = Commentary(
        title = "wow this tutorial changed my life",
        author= "Buy my ebook to get rich",
        date = datetime.datetime.utcnow(),
        content ="I have summarized what you said and couple of advices from elun Mosk and Joff bezez in my ebook",
        article_id = article2.id
    )
    db.session.add(mean_commentary1)
    db.session.add(mean_commentary2)
    db.session.add(mean_commentary3)
    db.session.add(mean_commentary4)
    db.session.commit()
