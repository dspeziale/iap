from flask import Blueprint

quadrature_bp = Blueprint('quadrature_bp', __name__)

@quadrature_bp.route('/reports')
def reports():
    return "Reports Page"
