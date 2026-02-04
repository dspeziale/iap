from api.index import app
from api.extensions import db
from api.models import Utente
from werkzeug.security import generate_password_hash
import sys

def create_admin():
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        # Check if admin exists
        email = "admin@iap.com"
        if Utente.query.filter_by(email=email).first():
            print(f"User {email} already exists.")
            return

        print(f"Creating admin user: {email}")
        admin = Utente(
            email=email,
            password_hash=generate_password_hash('admin'),
            nome='Admin',
            cognome='Global',
            ruolo='Administrator'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Login with: admin@iap.com / admin")

if __name__ == "__main__":
    create_admin()
