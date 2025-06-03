from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()   # Creates a SQLAlchemy object to handle database interactions
login_manager = LoginManager() # Creates a LoginManager to handle user sessions and authentication
login_manager.login_view = "auth.login"   # Route name for login

migrate = Migrate() # Creates a Migrate instance to manage database schema migrations
bcrypt = Bcrypt() # Creates a Bcrypt instance from flask_bcrypt for encryption of passwords

#Code ends here