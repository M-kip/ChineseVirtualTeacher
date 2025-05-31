from pymongo import MongoClient
from datetime import datetime
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.mongo_client = MongoClient(current_app.config['MONGO_URI'])
        g.db = g.mongo_client[current_app.config['MONGO_DBNAME']]
        g.db.command("ping")
        g.db.command("serverStatus")
        click.echo(f"Connected to MongoDB at {current_app.config['MONGO_URI']} on {datetime.now()}", err=True)
        click.echo(f"Using database: {current_app.config['MONGO_DBNAME']}", err=True)
    return g.db


def close_db(e=None):
    mongo_client = g.pop('mongo_client', None)

    if mongo_client is not None:
        mongo_client.close()

def init_db():
    """Initialize the database."""
    """Clear the existing data and create new tables."""
    """TODO: Implement database initialization logic."""
    # This function can be used to set up initial collections or data
    db = get_db()

@click.command('init-db')
def init_db_command():
    """Initialize the database."""
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)