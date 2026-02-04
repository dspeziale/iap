from functools import wraps
from flask import session, flash, redirect, url_for
from math import radians, cos, sin, asin, sqrt

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth_bp.login"))
            
            user_role = session.get("audit_role") # Assuming we store role in session
            # If we don't store role directly in session for security, we might query DB here
            # For now, let's assume session['role'] or similar is populated on login
            if user_role not in roles and "Administrator" not in roles: # Admin access backup
                 flash("Access denied.", "danger")
                 return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 6371000 for meters
    return c * r * 1000 # Return in meters
