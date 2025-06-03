from app.extensions import db
from datetime import datetime, timezone


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float) 
    status = db.Column(db.String, nullable=False, default='active') 
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    spot = db.relationship("ParkingSpot", back_populates="reservations") # Many to One relationship with ParkingSpot as many can wish to reserve a particular spot
    user = db.relationship("User", back_populates="reservations") # Many to One relationship with users One user can have many reservations

    def __str__(self):
        return f"<Reservation {self.id} (User {self.user_id}, Spot {self.spot_id})>"

    def __repr__(self):
        return self.__str__()
    
#Code ends here