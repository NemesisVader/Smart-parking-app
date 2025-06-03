from app.extensions import db, bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    reservations = db.relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    
    def __str__(self):
        return f'<User: {self.username}>'
    
    def __repr__(self):
        return self.__str__()
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
#Code ends here