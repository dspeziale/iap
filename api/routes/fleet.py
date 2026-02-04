from flask import Blueprint

fleet_bp = Blueprint('fleet_bp', __name__)

@fleet_bp.route('/fleet')
def fleet_dashboard():
    return "Fleet Dashboard"
