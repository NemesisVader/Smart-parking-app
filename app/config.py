import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') # Loads the Secret Key from my .env file for my app
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') # Loads the Database URI for my flask app( Thats where my database will be stored along with its name)
    
    
#Code ends here