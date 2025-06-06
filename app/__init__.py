from flask import Flask, render_template, url_for, session
from app.routes import route_handler, auth_bp
from app.config import Config
from app.extensions import db, login_manager, migrate, bcrypt
from app.models import *


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config) # Loads the settings (like SECRET_KEY and database URL) from the Config class in my config.py set FLASK_APP=run.py
    app.register_blueprint(auth_bp) # Register the authentication blueprint (handles login, register, logout routes)
    
    db.init_app(app) # Initialzes SQLAlchemy
    login_manager.init_app(app) # Initializes the LoginManager from flask_login
    
    @login_manager.user_loader
    def load_user(user_id):
        # Given a user ID (stored in the session), looks up and return the corresponding User object
        return User.query.get(int(user_id))
    
    migrate.init_app(app, db) # Initialize Flask-Migrate 
    bcrypt.init_app(app) # Initialize Bcrypt for encryption of passwords
    
    # Pretends like if the app is running so we can access the database when loading the app and perform the logic defined.
    with app.app_context(): 
        from app.seed import seed_admin
        seed_admin()  # Seeds the admin user after migrations

    route_handler(app, db) # Add the routes to my Flask app when executed
    return app

#Code ends here