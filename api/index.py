import os
from flask import Flask, render_template
from .extensions import db, migrate, sess
from .models import Utente # Import models so Alembic can detect them

# Import Blueprints
from .routes.auth import auth_bp
from .routes.scanner import scanner_bp
from .routes.admin import admin_bp
from .routes.fleet import fleet_bp
from .routes.projects import projects_bp
from .routes.quadrature import quadrature_bp
from sqlalchemy.pool import NullPool

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Vercel/Neon Config
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=db_url or 'sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='filesystem',
        SESSION_PERMANENT=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": NullPool
        }
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(scanner_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(fleet_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(quadrature_bp)

    # Global Auth Check
    from flask import session, request, redirect, url_for

    @app.before_request
    def require_login():
        # Allow static files
        if request.endpoint == 'static':
            return
            
        # Allow auth routes (login, logout)
        if request.endpoint and 'auth_bp' in request.endpoint:
            return
            
        # Require login for everything else
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login'))

    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Ensure database tables are created (for dev/sqlite)
    with app.app_context():
        db.create_all()

    return app

# For Vercel
app = create_app()
