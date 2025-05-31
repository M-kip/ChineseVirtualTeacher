# app/__init__.py
# app/MLAI/load_docs.py
"""This module provides functionality to load docs from a specified directory."""
import os
import array
from sentence_transformers import SentenceTransformer
from flask import current_app
import chardet
import fitz # PyMuPDF for PDF handling
embedding_model = "sentence-transformers/all-MiniLM-L6-v2" # embedding model/encoder
encoder = SentenceTransformer(embedding_model) # Encoder to handle the vectorization tasks
topK = 3

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def loadDocs(directory_path):
    """
    Load documents from a specified directory and preprocess them.
    Args:
        directory_path (str): The path to the directory containing the documents.       
    Returns:
        list: A list of dictionaries, each containing the text and path of a document.
    """ 
    docs__ = {}
    for filename in os.listdir(os.path.normcase(directory_path)):
        if filename.endswith(".pdf"): # assuming docs are all .pdf files
            filename_without_ext = os.path.splitext(filename)[0] # remove .txt extension
            file_path = os.path.join(directory_path, filename)
            with fitz.open(file_path) as doc:
                docs__[filename_without_ext] = [page.get_text() for page in doc]
            # Rearrage the chunks and prepend the name of the file 
            docs = [{'text': f"{filename }' | ' {section}", 'path': filename } for filename, sections in docs__.items() for section in sections]
    return docs

def get_embedding(docs):
    """
    Get the embedding for a given text using the pre-trained SentenceTransformer model.
    
    Args:
        doc (list): The text to be embedded.
        
    Returns:
        list: The embedding vector for the text.
    """
    # Define a list to store the data
    data = [{"id": idx, "vector_source": row['text'], "payload": row} for idx, row in enumerate(docs)]

    # Collect all text for batch encoding
    texts = [f"{row['vector_source']}" for row in data]

    # Encode all text for batch encoding
    print(f"======> encoding text with {embedding_model} encoder\n")
    embeddings = encoder.encode(texts, batch_size=32, show_progress_bar=True)

    # Assign the embeddings back to your data structure
    for row, embedding in zip(data, embeddings):
        row['vector'] = list(array.array("f", embedding))
    return data

def save_docs_to_db(docs, db):
    """
    Save the documents to the database.
    
    Args:
        docs (list): The list of documents to be saved.
        db: The database connection object.
    """
    print(f"======> Saving {len(docs)} docs to {current_app.config['MONGO_DBNAME']} table in the database\n")
    db.books.insert_many(docs)
    print(f"======> Saved {len(docs)} docs to {current_app.config['MONGO_DBNAME']} table in the database\n")

