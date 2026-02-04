from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Automezzo, Utente
from ..extensions import db
from ..utils import role_required
from ..traccar_client import TraccarClient

fleet_bp = Blueprint('fleet_bp', __name__)

# Mock Client - In prod usage, read config from env
traccar = TraccarClient("http://traccar:8082", "admin", "admin")

@fleet_bp.route('/fleet')
@role_required(['Administrator', 'Supervisor'])
def fleet_dashboard():
    vehicles = Automezzo.query.all()
    # Fetch live data
    positions = traccar.get_positions()
    
    # Merge db vehicle data with live positions (simple matching by traccar_id/deviceId)
    # For demo we jsut pass them separately
    return render_template('fleet.html', vehicles=vehicles, positions=positions)

@fleet_bp.route('/fleet/vehicle', methods=['POST'])
@role_required(['Administrator'])
def create_vehicle():
    targa = request.form.get('targa')
    modello = request.form.get('modello')
    traccar_id = request.form.get('traccar_id')
    
    if Automezzo.query.filter_by(targa=targa).first():
        flash('Vehicle already exists.', 'danger')
    else:
        new_vehicle = Automezzo(targa=targa, modello=modello, traccar_id=traccar_id)
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle added successfully.', 'success')
    return redirect(url_for('fleet_bp.fleet_dashboard'))

