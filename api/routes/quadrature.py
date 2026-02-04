from flask import Blueprint, render_template, request, send_file
from ..models import Timbratura, Utente
from ..extensions import db
from ..utils import role_required
import io
import openpyxl
from datetime import datetime, date, timedelta

quadrature_bp = Blueprint('quadrature_bp', __name__)

@quadrature_bp.route('/reports')
@role_required(['Administrator', 'Supervisor'])
def reports():
    return render_template('reports.html')

@quadrature_bp.route('/reports/generate', methods=['POST'])
@role_required(['Administrator', 'Supervisor'])
def generate_report():
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1) # inclusive
    
    # Fetch Data
    timbrature = Timbratura.query.filter(
        Timbratura.timestamp >= start_date,
        Timbratura.timestamp < end_date
    ).order_by(Timbratura.utente_id, Timbratura.timestamp).all()
    
    # Generate Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance Report"
    
    # Headers
    headers = ["Date", "User", "Type", "Time", "Site/Project", "Note", "Distance"]
    ws.append(headers)
    
    for t in timbrature:
        site_info = t.cantiere.nome if t.cantiere_id else "N/A"
        row = [
            t.timestamp.date(),
            f"{t.utente.nome} {t.utente.cognome}",
            t.tipo,
            t.timestamp.time(),
            site_info,
            t.server_note or "",
            t.distanza
        ]
        ws.append(row)
        
    # Save to BytesIO
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    filename = f"Report_{start_date_str}_{end_date_str}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

