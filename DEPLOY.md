# Deployment Guide: Vercel + Neon

Follow these steps to deploy Impulse to production.

## 1. Database Setup (Neon)
1.  Go to [Neon Console](https://console.neon.tech/).
2.  Create a new Project.
3.  Copy the **Connection String** (Pooled connection recommended).
    *   Format: `postgres://user:pass@host/db...`

## 2. Vercel Deployment
1.  Install Vercel CLI:
    ```bash
    npm install -g vercel
    ```
2.  Login:
    ```bash
    vercel login
    ```
3.  Deploy (Run in project root):
    ```bash
    vercel
    ```
    *   Set up and deploy? [Y]
    *   Which scope? [Select your team/user]
    *   Link to existing project? [N]
    *   Project Name? [impulse-app]
    *   In which directory is your code located? [./]
    *   Auto-detect settings? [N] -> **Important**:
        *   Build Command: `# None` (Leave empty or space)
        *   Output Directory: `public` (or default)
        *   Install Command: `pip install -r requirements.txt`

## 3. Environment Variables
Once the project is created on Vercel:
1.  Go to the Vercel Dashboard -> Settings -> Environment Variables.
2.  Add the following:
    *   `DATABASE_URL`: [Paste your Neon Connection String]
    *   `SECRET_KEY`: [Generate a random strong string]

3.  **Redeploy** for variables to take effect:
    ```bash
    vercel --prod
    ```

## 4. Initialize Database
Since Vercel is serverless, you cannot run `flask db upgrade` easily in shell. The app is configured to attempt `db.create_all()` on startup (`api/index.py`), but for a cleaner setup, you can run a script locally connected to the remote DB *OR* create a temporary route.

**Recommended**: Use your local machine to initialize the remote DB.
1.  Set the env var locally:
    ```powershell
    $env:DATABASE_URL = "postgres://..."
    ```
2.  Run the python shell:
    ```python
    from api.index import app
    from api.extensions import db
    from api.models import Utente
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        db.create_all()
        # Create Admin
        admin = Utente(email='admin@iap.com', password_hash=generate_password_hash('admin_password'), nome='Admin', cognome='Global', ruolo='Administrator')
        db.session.add(admin)
        db.session.commit()
    ```

## 5. Done!
Visit your Vercel URL (e.g., `https://impulse-app.vercel.app`).
