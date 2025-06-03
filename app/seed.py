from app.extensions import db
from app.models import User
from dotenv import load_dotenv
import os

load_dotenv()

def seed_admin():
    if not User.query.filter_by(is_admin=True).first():
        admin = User(
            username=os.getenv('ADMIN_NAME'),
            email=os.getenv('ADMIN_EMAIL'),
            is_admin=True
        )
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
