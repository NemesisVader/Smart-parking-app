from app.routes.auth import *
from app.routes.admin import *
from flask import render_template

def route_handler(app, db):
    
    @app.route('/')  # My first route where the user lands when he/she searches for the website on any Search Engine.
    def index():
        return render_template('index.html')
    
#Code ends here