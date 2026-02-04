from .extensions import db
from datetime import datetime

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    ruolo = db.Column(db.String(20), default='User') # Administrator, Supervisor, Operator, User
    otp_secret = db.Column(db.String(32))
    working_hours_start = db.Column(db.Time, nullable=True)
    working_hours_end = db.Column(db.Time, nullable=True)
    
    # Self-referential relationship for Supervisor
    supervisor_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=True)
    subordinates = db.relationship('Utente', backref=db.backref('supervisor', remote_side=[id]))

class Timbratura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False) # IN, OUT, ASSENZA
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    accuracy = db.Column(db.Float)
    distanza = db.Column(db.Float) # Distance from site center
    server_note = db.Column(db.String(255))
    
    cantiere_id = db.Column(db.Integer, db.ForeignKey('cantiere.id'), nullable=True)
    commessa_id = db.Column(db.Integer, db.ForeignKey('commessa.id'), nullable=True)
    
    utente = db.relationship('Utente', backref='timbrature')

class Cantiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    indirizzo = db.Column(db.String(255))
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    raggio = db.Column(db.Integer, default=50) # Geofence radius in meters
    qr_code_secret = db.Column(db.String(64), unique=True)
    attivo = db.Column(db.Boolean, default=True)
    
    commessa_id = db.Column(db.Integer, db.ForeignKey('commessa.id'), nullable=True)

class Commessa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codice = db.Column(db.String(50), unique=True, nullable=False)
    descrizione = db.Column(db.String(255))
    
    cantieri = db.relationship('Cantiere', backref='commessa')

class Automezzo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    targa = db.Column(db.String(20), unique=True, nullable=False)
    modello = db.Column(db.String(100))
    traccar_id = db.Column(db.Integer, unique=True) # Linked to external Traccar Device ID
    fuel_card = db.Column(db.String(50))
    
    driver_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=True)
    driver = db.relationship('Utente', backref='automezzo')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), default='info') # info, warning, error
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text)

class Overtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(20), default='PENDING') # PENDING, APPROVED, REJECTED
    
    utente = db.relationship('Utente', backref='overtime_requests')

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    utente_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45))
    details = db.Column(db.Text)
