from flask import render_template, request
from datetime import datetime
from . import main

current_time = datetime.now()
@main.route('/')
def index():
    current_time = datetime.now()
    return render_template('main/index.html', time=current_time)

@main.route('/vector_search', methods=['GET', 'POST'])
def vector_search():
    query_text = request.args.get('query_txt', '')
    if request.method == 'GET' and query_text:
        # If GET request with query_txt, perform vector search
        limit = int(request.args.get('limit', 10))
        num_candidates = int(request.args.get('num_candidates', 30))
        #print(f"Received query: {query_text}, limit: {limit}, num_candidates: {num_candidates}")
        from app.models import perform_vector_search
        results = perform_vector_search(query_text, limit, num_candidates)
        #print(f"Search results: {results}")
        # Render the vector search results

        return render_template('main/vector_search.html', results=results, query=query_text, time=current_time)
    return render_template('main/vector_search.html', time=current_time)

@main.route('/ai_recommendations', methods=['GET', 'POST'])
def ai_recommendations():
    query_text = request.args.get('query_txt', '')
    if request.method == 'GET' and query_text:
        # If GET request with query_txt, perform AI recommendations
        limit = int(request.args.get('limit', 10))
        num_candidates = int(request.args.get('num_candidates', 30))
        #print(f"Received query: {query_text}, limit: {limit}, num_candidates: {num_candidates}")
        from app.models import generate_response, perform_vector_search
        results = perform_vector_search(query_text, limit, num_candidates)
        ai_results = generate_response(query_text, results)
        print(f"Recommendations results: {ai_results}")
        # Render the AI recommendations results

        return render_template('main/AI_recommendations.html', results=ai_results, query=query_text, time=current_time)
    return render_template('main/AI_recommendations.html', time=current_time)