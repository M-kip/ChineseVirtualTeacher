from flask import current_app
from .db import get_db
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def perform_vector_search(query_text, limit=10, num_candidates=None):
    if num_candidates is None:
        num_candidates = limit * 3

    try:
        db = get_db()
        collection = db[current_app.config['MONGO_COLLECTION']]

        # Get vector embedding of query
        query_vector = model.encode(query_text).tolist()

        # Perform knnBeta vector search
        results = collection.aggregate([
            {
                '$vectorSearch': {
                    'index': 'hsk_vector_search',  # your Lucene vector index name
                    'queryVector': query_vector,
                    'path': 'vector',
                    'numCandidates': num_candidates,
                    'limit': limit
                }
            },
            {'$project': {
                '_id': 0,
                'text': '$vector_source',
                'path': '$payload.path',
                'score': {'$meta': 'searchScore'}
            }},
            {'$sort': {'score': -1}},
            {'$limit': limit}
        ])

        return list(results)
    except Exception as e:
        print(f"Error during vector search: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    query = "What does the finals and intials in chinese mean?"
    results = perform_vector_search(query, limit=5)
    for result in results:
        print(result)