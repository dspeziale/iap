from flask import Blueprint

scanner_bp = Blueprint('scanner_bp', __name__)

@scanner_bp.route('/scanner')
def scanner():
    return "Scanner Page"
