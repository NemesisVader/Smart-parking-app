from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime, timezone
from flask_login import login_required, current_user
from app.models import ParkingLot, Reservation, ParkingSpot
from app.extensions import db


user_bp = Blueprint('user', __name__)

@user_bp.route('/user/dashboard', endpoint='dashboard')
@login_required
def user_dashboard():
    active_res = Reservation.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).order_by(Reservation.parking_timestamp.desc()).all()


    past_res = (
        Reservation.query
        .filter(
            Reservation.user_id == current_user.id,
            Reservation.status != 'active'
        )
        .order_by(Reservation.parking_timestamp.asc())
        .limit(5)
        .all()
    )

    lots = ParkingLot.query.all()
    lots_data = []
    for lot in lots:
        spots = [
            {"id": s.id, "spot_number": s.spot_number, "status": s.status}
            for s in lot.spots
        ]
        lots_data.append({
            "id":            lot.id,
            "location_name": lot.prime_location_name,
            "num_spots":     lot.num_spots,
            "price":         lot.price_per_hour,
            "address":       lot.address,
            "pincode":       lot.pincode,
            "spots":         spots
        })

    return render_template(
        'user/dashboard.html',
        user=current_user,
        active_res=active_res,
        past_res=past_res,
        lots=lots_data
    )
  
@user_bp.route('/user/reserve', methods=['POST'])
@login_required
def reserve_spot():
    lot_id = request.form.get('lot_id')
    if not lot_id:
        flash("Invalid parking lot selection.", "danger")
        return redirect(url_for('user.dashboard'))

    # Auto-pick the first available spot from this lot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        flash("Sorry, no available spots in this lot.", "danger")
        return redirect(url_for('user.dashboard'))

    # Create reservation
    reservation = Reservation(
        user_id=current_user.id,
        spot_id=spot.id,
        parking_timestamp=datetime.now(timezone.utc),
        status='active',
        parking_cost=0
    )
    spot.status = 'R'

    db.session.add(reservation)
    db.session.commit()

    flash(f"Reserved Spot #{spot.spot_number} at {spot.lot.prime_location_name}.", "success")
    return redirect(url_for('user.dashboard'))


@user_bp.route('/user/complete_reservation', methods=['POST'])
@login_required
def complete_reservation():
    res_id = request.form.get('reservation_id')
    res = Reservation.query.filter_by(
        id=res_id, user_id=current_user.id, status='active'
    ).first_or_404()

    # 1) Set leaving time
    res.leaving_timestamp = datetime.utcnow()

    # 2) Calculate cost: hours * rate
    delta = res.leaving_timestamp - res.parking_timestamp
    hours = delta.total_seconds() / 3600
    rate = res.spot.lot.price_per_hour
    res.parking_cost = round(hours * rate, 2)

    # 3) Mark reservation completed
    res.status = 'completed'

    # 4) Free up the spot
    res.spot.status = 'A'

    db.session.commit()
    flash(f"Reservation ended. Total cost ₹{res.parking_cost}.", "success")
    return redirect(url_for('user.dashboard'))
