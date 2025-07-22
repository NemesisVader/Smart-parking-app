# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import ParkingLot, ParkingSpot, Reservation
from app.forms.LotForm import LotForm
from app.extensions import db
from sqlalchemy import func, cast, Date

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Unauthorized Entry", 'danger')
        return redirect(url_for('auth.login'))

    lots = ParkingLot.query.all()

    # Optional summary stats
    total_spots = sum(lot.num_spots for lot in lots)
    total_revenue = (
        db.session.query(func.sum(Reservation.parking_cost))
        .scalar() or 0
    )
    occupied_spots = (
        ParkingSpot.query
        .filter_by(status='O')
        .count()
    )

    return render_template(
        'admin/dashboard.html',
        lots=lots,
        total_spots=total_spots,
        total_revenue=total_revenue,
        occupied_spots=occupied_spots
    )

@admin_bp.route('/admin/lots/create', methods=['GET', 'POST'])
@login_required
def create_lot():
    if not current_user.is_admin:
        flash("Unauthorized Entry", 'danger')
        return redirect(url_for('auth.login'))

    form = LotForm()
    if form.validate_on_submit():
        print("Form validated!")
        lot = ParkingLot(
            prime_location_name=form.prime_location_name.data,
            price_per_hour=float(form.price_per_hour.data),
            num_spots=form.num_spots.data,
            address=form.address.data,
            pincode=form.pincode.data
        )
        db.session.add(lot)
        db.session.commit() 

        for i in range(1, lot.num_spots + 1):
            spot = ParkingSpot(
                lot_id=lot.id,
                spot_number=str(i),
                status= 'A'
            )
            db.session.add(spot)
        db.session.commit()

        flash(f"Parking Lot '{lot.prime_location_name}' created with {lot.num_spots} spots!", 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        for field_name, errors in form.errors.items():
            for err in errors:
                flash(f"{getattr(form, field_name).label.text}: {err}", "danger")
                
    return render_template('admin/create_lot.html', form=form)

@admin_bp.route('/admin/lots/<int:lot_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lot(lot_id):
    if not current_user.is_admin:
        flash("Unauthorized Entry", 'danger')
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    form = LotForm(obj=lot)

    if form.validate_on_submit():
        lot.prime_location_name = form.prime_location_name.data
        lot.price_per_hour = float(form.price_per_hour.data)
        lot.address = form.address.data
        lot.pincode = form.pincode.data
        db.session.commit()
        flash(f"Lot '{lot.prime_location_name}' updated successfully!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template("admin/edit_lot.html", form=form, lot=lot)

@admin_bp.route('/admin/lots/<int:lot_id>/delete', methods=['POST'])
@login_required
def delete_lot(lot_id):
    if not current_user.is_admin:
        flash("Unauthorized Entry", "danger")
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)

    db.session.delete(lot)
    db.session.commit()

    flash(f"Lot '{lot.prime_location_name}' has been deleted.", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route(
    '/admin/lots/<int:lot_id>/spots/<int:spot_id>',
    methods=['GET', 'POST']
)
@login_required
def spot_detail(lot_id, spot_id):
    if not current_user.is_admin:
        flash("Unauthorized Entry", "danger")
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    spot = ParkingSpot.query.get_or_404(spot_id)
    # Current active reservation for this spot:
    active_res = Reservation.query \
        .filter_by(spot_id=spot.id, status='active') \
        .first()

    # Past (non-active) reservations:
    past_res = Reservation.query \
        .filter(
            Reservation.spot_id == spot.id,
            Reservation.status != 'active'
        ) \
        .order_by(Reservation.parking_timestamp.desc()) \
        .all()

    if request.method == 'POST':
        if active_res:
            active_res.status = 'cancelled'
            spot.status = 'A' 
            db.session.commit()
            flash(f"Released spot {spot.spot_number} from user {active_res.user.email}.", "success")
        return redirect(
            url_for('admin.spot_detail', lot_id=lot.id, spot_id=spot.id)
        )

    return render_template(
        'admin/spot_detail.html',
        lot=lot,
        spot=spot,
        active_res=active_res,
        past_res=past_res
    )

@admin_bp.route('/admin/lots/<int:lot_id>/analytics')
@login_required
def lot_analytics(lot_id):
    if not current_user.is_admin:
        flash("Unauthorized Entry", "danger")
        return redirect(url_for('auth.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    return render_template('admin/lot_analytics.html', lot=lot)

@admin_bp.route('/admin/lots/<int:lot_id>/analytics/data')
@login_required
def lot_analytics_data(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    # Revenue: sum of parking_cost for completed reservations
    revenue = (
        db.session.query(db.func.sum(Reservation.parking_cost))
        .join(ParkingSpot)
        .filter(ParkingSpot.lot_id == lot.id)
        .scalar() or 0
    )

    # Occupancy: number of spots currently reserved/occupied
    occupied = ParkingSpot.query.filter(
        ParkingSpot.lot_id == lot.id,
        ParkingSpot.status != 'A'  # not available => occupied
    ).count()

    return jsonify({
        "revenue": [
            {
                "lot": lot.prime_location_name,
                "revenue": revenue
            }
        ],
        "occupancy": [
            {
                "lot": lot.prime_location_name,
                "occupied": occupied,
                "total": lot.num_spots
            }
        ]
    })

#Code Ends here