import os
import click

from dotenv import load_dotenv
from flask.cli import FlaskGroup
from app.main import create_app, db
from app import blueprint

load_dotenv()

@click.command()
def run():
    """ Launching the app"""
    app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
    app.register_blueprint(blueprint)
    app.run(host=os.getenv('APP_HOST') or '0.0.0.0', port=os.getenv('APP_PORT') or '5000')

@click.command()
def test():
    """Launching the batch of tests with Pytest"""

if __name__ == '__main__':
    run()