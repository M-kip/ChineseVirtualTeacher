from flask import render_template
from datetime import datetime
from . import main

@main.route('/')
def index():
    current_time = datetime.now()
    return render_template('main/index.html', time=current_time)