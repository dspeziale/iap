from flask import Blueprint

projects_bp = Blueprint('projects_bp', __name__)

@projects_bp.route('/projects')
def projects_dashboard():
    return "Projects Dashboard"
