from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import ParkingLot, Reservation
from app.utils.mapbox_util import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/dashboard', endpoint='dashboard')
@login_required
def user_dashboard():
    active_res = Reservation.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).first()

    past_res = (
        Reservation.query
        .filter(
            Reservation.user_id == current_user.id,
            Reservation.status != 'active'
        )
        .order_by(Reservation.parking_timestamp.desc())
        .limit(5)
        .all()
    )

    lots = ParkingLot.query.all()
    lots_data = []

    for lot in lots:
        full_address = f"{lot.prime_location_name}, {lot.address}, {lot.pincode}"
        lat, lng = get_mapbox_coords(full_address)

        if lat is None or lng is None:
            print(f"[WARN] Could not geocode: {full_address}")
            continue

        lots_data.append({
            'id':             lot.id,
            'location_name':  lot.prime_location_name,
            'price_per_hour': lot.price_per_hour,
            'num_spots':      lot.num_spots,
            'address':        lot.address,
            'pincode':        lot.pincode,
            'lat':            lat,
            'lng':            lng
        })

    return render_template(
        'user/dashboard.html',
        user=current_user,
        active_res=active_res,
        past_res=past_res,
        lots=lots_data
    )
