from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from ..models import Utente, Setting
from ..extensions import db
from ..utils import role_required

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin')
@role_required(['Administrator'])
def admin_dashboard():
    return render_template('admin/dashboard.html') # Placeholder, or redirect to users

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@role_required(['Administrator'])
def manage_users():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            nome = request.form.get('nome')
            cognome = request.form.get('cognome')
            email = request.form.get('email')
            password = request.form.get('password')
            ruolo = request.form.get('ruolo')
            
            if Utente.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
            else:
                new_user = Utente(
                    nome=nome,
                    cognome=cognome,
                    email=email,
                    password_hash=generate_password_hash(password),
                    ruolo=ruolo
                )
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully.', 'success')
                
        elif action == 'delete':
            user_id = request.form.get('user_id')
            user = Utente.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully.', 'success')
                
    users = Utente.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/settings', methods=['GET', 'POST'])
@role_required(['Administrator'])
def settings():
    if request.method == 'POST':
        for key, value in request.form.items():
            setting = Setting.query.get(key)
            if setting:
                setting.value = value
            else:
                db.session.add(Setting(key=key, value=value))
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        
    settings_list = Setting.query.all()
    # Convert list to dict for easy access in template
    settings_dict = {s.key: s.value for s in settings_list}
    return render_template('impostazioni.html', settings=settings_dict)

