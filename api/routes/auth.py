from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from ..models import Utente, Setting
from ..extensions import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Helper for First Run (Setup Admin)
    user_count = Utente.query.count()
    first_run = (user_count == 0)

    if request.method == 'POST':
        # Hook for setup
        if first_run and request.form.get('action') == 'setup':
            from werkzeug.security import generate_password_hash
            admin_email = "admin@iap.com"
            admin_pass = request.form.get('admin_password')
            
            if not admin_pass:
                flash("Password required.", "danger")
                return render_template('login.html', first_run=True)

            admin = Utente(
                email=admin_email,
                password_hash=generate_password_hash(admin_pass),
                nome='Admin',
                cognome='Global',
                ruolo='Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            flash(f"Admin created! Login with {admin_email}", "success")
            return redirect(url_for('auth_bp.login'))

        # Normal Login Flow
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Utente.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = f"{user.nome} {user.cognome}"
            session['audit_role'] = user.ruolo
            
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html', first_run=first_run)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_bp.login'))

