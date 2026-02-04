import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import create_app...")
    from api.index import create_app
    print("Import successful. Creating app...")
    app = create_app()
    print("App created successfully!")
    
    print("Verifying database models...")
    with app.app_context():
        from api.extensions import db
        db.create_all()
        print("Database tables created (if using SQLite).")
        
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
