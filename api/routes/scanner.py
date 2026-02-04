from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from ..models import Cantiere, Timbratura, Utente, Notification
from ..extensions import db
from ..utils import role_required, get_distance

scanner_bp = Blueprint('scanner_bp', __name__)

@scanner_bp.route('/scanner')
@role_required(['User', 'Operator', 'Supervisor', 'Administrator'])
def scanner():
    return render_template('scanner.html')

@scanner_bp.route('/api/scan', methods=['POST'])
@role_required(['User', 'Operator', 'Supervisor', 'Administrator'])
def scan_endpoint():
    data = request.json
    qr_code = data.get('qr_code')
    lat = data.get('lat')
    lon = data.get('lon')
    accuracy = data.get('accuracy', 0)
    
    user_id = session.get('user_id')
    user = Utente.query.get(user_id)
    
    # 1. Find Cantiere by QR Secret
    cantiere = Cantiere.query.filter_by(qr_code_secret=qr_code).first()
    if not cantiere:
        return jsonify({'status': 'error', 'message': 'Invalid QR Code.'}), 400
    
    if not cantiere.attivo:
         return jsonify({'status': 'error', 'message': 'This site is not active.'}), 400

    # 2. Check Distance (Geofence)
    distance = get_distance(lat, lon, cantiere.lat, cantiere.lon)
    valid_radius = cantiere.raggio + float(accuracy) + 20 # Add buffer
    
    if distance > valid_radius:
         return jsonify({
             'status': 'error', 
             'message': f'You are too far from the site ({int(distance)}m). Move closer.'
         }), 400
         
    # 3. Determine IN vs OUT
    # Look for the last punch for this user today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    last_punch = Timbratura.query.filter(
        Timbratura.utente_id == user_id,
        Timbratura.timestamp >= today_start
    ).order_by(Timbratura.timestamp.desc()).first()
    
    tipo = 'IN'
    if last_punch andBN last_punch.tipo == 'IN':
        tipo = 'OUT'
        
    # 4. Create Record
    t = Timbratura(
        utente_id=user.id,
        tipo=tipo,
        lat=lat,
        lon=lon,
        accuracy=accuracy,
        distanza=distance,
        cantiere_id=cantiere.id,
        commessa_id=cantiere.commessa_id
    )
    
    # 5. Check Schedule (Server Note)
    server_note = None
    if tipo == 'OUT' and user.working_hours_end:
         # Simplified check: timestamps are naive UTC in DB, careful with timezones
         pass 

    t.server_note = server_note
    db.session.add(t)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': f'Successfully clocked {tipo} at {cantiere.nome}',
        'tipo': tipo,
        'timestamp': t.timestamp.isoformat()
    })

