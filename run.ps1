# Startup Script for Impulse
Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Setting environment variables..."
$env:FLASK_APP = "api.index"
$env:FLASK_ENV = "development"

Write-Host "Creating Database tables..."
# Using a temporary python snippet to ensure tables exist
python -c "from api.index import app; from api.extensions import db; ctx = app.app_context(); ctx.push(); db.create_all(); print('Database verified.');"

Write-Host "Starting Flask Server..."
flask run
