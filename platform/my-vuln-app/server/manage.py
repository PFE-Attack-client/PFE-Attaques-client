import os
import click

from dotenv import load_dotenv
from flask.cli import FlaskGroup
from app.main import create_app, db
from app import blueprint
from flask_migrate import Migrate, migrate, upgrade, init
from app.main.model import user
from app.main.model import article
from app.main.seed import seed_the_db, seed_commentaries

load_dotenv()

@click.group()
def cli1():
    pass

@cli1.command()
def run():
    """ Launching the app"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    app.register_blueprint(blueprint)
    app.run(host=os.getenv('APP_HOST') or '0.0.0.0', port=os.getenv('APP_PORT') or '5000')

@click.group()
def cli2():
    pass

@cli2.command()
def test():
    """Launching the batch of tests with Pytest"""
    print("testing...")

@click.group()
def cli3():
    pass

@cli3.command()
def initdb():
    """Init the migrations files for the database"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    Migrate(app=app, db=db)
    with app.app_context():
        init(directory="app/main/migrations")

@click.group()
def cli4():
    pass

@cli4.command()
def upgradedb():
    """Upgrade the database"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    Migrate(app=app, db=db)
    with app.app_context():
        upgrade(directory="app/main/migrations")

@click.group()
def cli5():
    pass

@cli5.command()
def migratedb():
    """Migrate the database"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    Migrate(app=app, db=db)
    with app.app_context():
        migrate(directory="app/main/migrations")

@click.group()
def cli6():
    pass

@cli6.command()
def seeddb():
    """Fill the database with the initial seed"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    with app.app_context():
        #seed_the_db()
        seed_commentaries()


cli = click.CommandCollection(sources=[cli1, cli2, cli3, cli4, cli5, cli6])
if __name__ == '__main__':
    cli()