from flask import Blueprint, render_template, request, redirect, url_for, flash
import uuid
from ..models import Commessa, Cantiere
from ..extensions import db
from ..utils import role_required

projects_bp = Blueprint('projects_bp', __name__)

@projects_bp.route('/projects')
@role_required(['Administrator', 'Supervisor'])
def projects_dashboard():
    commesse = Commessa.query.all()
    return render_template('projects.html', commesse=commesse)

@projects_bp.route('/projects/create_commessa', methods=['POST'])
@role_required(['Administrator'])
def create_commessa():
    codice = request.form.get('codice')
    descrizione = request.form.get('descrizione')
    
    if Commessa.query.filter_by(codice=codice).first():
        flash('Commessa code already exists.', 'danger')
    else:
        new_commessa = Commessa(codice=codice, descrizione=descrizione)
        db.session.add(new_commessa)
        db.session.commit()
        flash('Commessa created successfully.', 'success')
    return redirect(url_for('projects_bp.projects_dashboard'))

@projects_bp.route('/projects/create_cantiere', methods=['POST'])
@role_required(['Administrator'])
def create_cantiere():
    commessa_id = request.form.get('commessa_id')
    nome = request.form.get('nome')
    indirizzo = request.form.get('indirizzo')
    lat = float(request.form.get('lat', 0))
    lon = float(request.form.get('lon', 0))
    raggio = int(request.form.get('raggio', 50))
    
    # Generate a unique secret for QR Code
    qr_secret = str(uuid.uuid4())
    
    new_cantiere = Cantiere(
        nome=nome,
        indirizzo=indirizzo,
        lat=lat,
        lon=lon,
        raggio=raggio,
        qr_code_secret=qr_secret,
        commessa_id=commessa_id
    )
    db.session.add(new_cantiere)
    db.session.commit()
    flash('Cantiere created successfully.', 'success')
    return redirect(url_for('projects_bp.projects_dashboard'))

