import os
import re
from functools import wraps
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash
from cachetools import TTLCache
import time

# Feature flag for rate limiting
ENABLE_RATE_LIMITING = os.environ.get('ENABLE_RATE_LIMITING', 'True').lower() == 'true'

# Initialize in-memory store for request tracking
# Key format: f"{user_key}:requests", Value: [timestamp1, timestamp2, ...]
rate_limit_store = TTLCache(maxsize=10000, ttl=3600)


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        for old, new in [("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;"), ("'", "&#x27;")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_user_tier(db, user_id):
    """
    Fetch user's rate limit tier from database.
    
    Args:
        db: CS50 SQL database instance
        user_id: User ID to look up
        
    Returns:
        str: Rate limit tier ('free', 'premium', etc.)
    """
    if user_id is None:
        return "unauthenticated"
    
    try:
        rows = db.execute(
            "SELECT tier FROM rate_limit_configs WHERE user_id = ?",
            user_id
        )
        return rows[0]["tier"] if rows else "free"
    except Exception:
        # TODO: Log database errors appropriately
        return "free"


def rate_limit(tier_limits=None):
    """
    Decorator to enforce rate limits on routes.
    
    Tracks requests per user (authenticated) or IP (unauthenticated) and enforces
    per-minute and per-hour limits based on user tier.
    
    Args:
        tier_limits: Optional dict of rate limit tiers. Default:
            {
                "free": {"per_minute": 10, "per_hour": 100},
                "premium": {"per_minute": 100, "per_hour": 10000},
                "unauthenticated": {"per_minute": 5, "per_hour": 50}
            }
    
    Returns:
        Decorator function that wraps routes
        
    Example:
        @app.route("/group")
        @login_required
        @rate_limit()
        def group():
            pass
    """
    if tier_limits is None:
        tier_limits = {
            "free": {"per_minute": 10, "per_hour": 100},
            "premium": {"per_minute": 100, "per_hour": 10000},
            "unauthenticated": {"per_minute": 5, "per_hour": 50}
        }
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not ENABLE_RATE_LIMITING:
                return f(*args, **kwargs)
            
            # Import here to avoid circular dependency
            from app import db
            
            # Determine user identity and tier
            user_id = session.get("user_id")
            if user_id is None:
                user_tier = "unauthenticated"
                user_key = f"anon:{request.remote_addr}"
            else:
                user_tier = get_user_tier(db, user_id)
                user_key = f"user:{user_id}"
            
            # Build cache key for this endpoint
            endpoint_key = f"{user_key}:{f.__name__}:requests"
            
            # Initialize or retrieve request log
            if endpoint_key not in rate_limit_store:
                rate_limit_store[endpoint_key] = []
            
            now = time.time()
            requests = rate_limit_store[endpoint_key]
            
            # TODO: Implement sliding window algorithm for more accuracy
            # Current implementation: simple list of timestamps
            
            # Clean old requests (older than 1 hour)
            requests = [ts for ts in requests if now - ts < 3600]
            rate_limit_store[endpoint_key] = requests
            
            # Check per-minute limit
            limit_config = tier_limits.get(user_tier, tier_limits["free"])
            recent_requests = [ts for ts in requests if now - ts < 60]
            
            if len(recent_requests) >= limit_config["per_minute"]:
                # Log rate limit violation
                try:
                    db.execute(
                        "INSERT INTO rate_limit_logs (user_id, endpoint, status_code) VALUES (?, ?, ?)",
                        user_id,
                        f.__name__,
                        429
                    )
                except Exception:
                    # TODO: Log database errors appropriately
                    pass
                
                return apology(
                    f"Rate limit exceeded. Maximum {limit_config['per_minute']} requests per minute. Try again in 1 minute.",
                    429
                )
            
            # Check per-hour limit
            if len(requests) >= limit_config["per_hour"]:
                try:
                    db.execute(
                        "INSERT INTO rate_limit_logs (user_id, endpoint, status_code) VALUES (?, ?, ?)",
                        user_id,
                        f.__name__,
                        429
                    )
                except Exception:
                    # TODO: Log database errors appropriately
                    pass
                
                return apology(
                    f"Rate limit exceeded. Maximum {limit_config['per_hour']} requests per hour. Try again in 1 hour.",
                    429
                )
            
            # Record this request
            requests.append(now)
            rate_limit_store[endpoint_key] = requests
            
            # Call the actual route handler
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
