from pymongo import MongoClient
from datetime import datetime
import click
from flask import current_app, g
from .load_docs import loadDocs, get_embedding, save_docs_to_db

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

def initialize_docs(directory_path):
    """
    Initialize the documents in the database.
    
    Args:
        directory_path (str): The path to the directory containing the documents.
    """
    db = get_db()
    docs = loadDocs(directory_path)
    if docs:
        docs_with_embeddings = get_embedding(docs)
        save_docs_to_db(docs_with_embeddings, db)
    else:
        print("No documents found to load.")
        
def init_db():
    """Initialize the database."""
    """Clear the existing data and create new tables."""
    """TODO: Implement database initialization logic."""
    # This function can be used to set up initial collections or data
    initialize_docs(current_app.config['DOC_DIRECTORY'])

@click.command('init-db')
def init_db_command():
    """Initialize the database."""
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)