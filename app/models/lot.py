from app.extensions import db
from datetime import datetime, timezone


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key = True)
    prime_location_name = db.Column(db.String, nullable = False)
    price_per_hour = db.Column(db.Float, nullable = False)
    num_spots = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String, nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    spots = db.relationship("ParkingSpot", back_populates="lot", cascade="all, delete-orphan") # This ensures that if any Parking Lot is deleted all the related spots are deleted too and is One to Many relationship with Parking Spot.

    def __str__(self):
        return f"<ParkingLot: {self.prime_location_name}>"

    def __repr__(self):
        return self.__str__()
    
#Code ends here