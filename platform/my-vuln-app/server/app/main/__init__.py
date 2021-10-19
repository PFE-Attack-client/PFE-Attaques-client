from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from .config.config import config_by_name
from .config.db import db_sqlAlchemy as db

migrate = Migrate()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    print(f"[INIT] Creating app for {config_name} purpose.")
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    flask_bcrypt.init_app(app)
    return app