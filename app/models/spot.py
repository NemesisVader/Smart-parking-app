from app.extensions import db
from datetime import datetime, timezone


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key = True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"), nullable = False)
    spot_number = db.Column(db.String, nullable = False)
    status = db.Column(db.String(1), default = 'A', nullable = False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    lot = db.relationship("ParkingLot", back_populates="spots") # Many to One relation with parkinglot i.e Many spots can be under One ParkingLot
    reservations = db.relationship("Reservation", back_populates="spot", cascade="all, delete-orphan") # One spot can have many reservations over time and may form a WaitList.
    
    def __str__(self):
        return f'<ParkingSpot : {self.spot_number}>'
    
    def __repr__(self):
        return self.__str__()
    
#Code ends here