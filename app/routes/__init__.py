from flask import Flask

def route_handler(app, db):
    
    @app.route('/')  # My first route where the user lands when he/she searches for the website on any Search Engine.
    def index():
        return "Hello this is my flask app for my parking app."
    
    
    
#Code ends here