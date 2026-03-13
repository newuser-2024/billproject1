import os
from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_session import Session
from cs50 import SQL
from helpers import apology, login_required, track_event, should_send_notification
from email_service import EmailService
from tasks import (
    send_join_notification,
    send_expense_notification,
    send_settlement_notification,
)

# Configure application
app = Flask(__name__)

# Feature flag for email notifications
ENABLE_EMAIL_NOTIFICATIONS = (
    os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bill_splitter.db")

# Initialize email service (for health checks, not direct sending)
email_service = EmailService()


@app.route("/")
def index():
    """Display dashboard or redirect to login."""
    # TODO: Implement index route
    # If user logged in: show list of groups
    # Otherwise: show login page or welcome message
    pass


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # TODO: Implement user registration
    # GET: Render registration form
    # POST:
    #   - Get username, email, password from form
    #   - Validate inputs (not empty, email format)
    #   - Check if username already exists
    #   - Hash password
    #   - INSERT into users table with email field
    #   - If ENABLE_EMAIL_NOTIFICATIONS:
    #     - Create default user_preferences row
    #     - Optionally: queue email verification task (future)
    #   - Log event: track_event('user.registered', {'user_id': new_user_id})
    #   - Redirect to login
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    # TODO: Implement user login
    # GET: Render login form
    # POST:
    #   - Get username, password from form
    #   - Query users table
    #   - Verify password
    #   - Set session["user_id"]
    #   - Redirect to index or groups page
    pass


@app.route("/logout")
def logout():
    """Log user out."""
    # TODO: Implement user logout
    # Clear session["user_id"] and session["group_id"]
    # Redirect to login
    pass


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new group."""
    # TODO: Implement group creation
    # GET: Render create group form
    # POST:
    #   - Get group_name from form
    #   - Validate not empty
    #   - INSERT into groups table
    #   - INSERT creator into group_users table
    #   - Set session["group_id"]
    #   - If ENABLE_EMAIL_NOTIFICATIONS:
    #     - Log event: track_event('group.created', {...})
    #   - Redirect to group page
    pass


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    """Join an existing group."""
    # TODO: Implement group join with email notification
    # GET: Render join group form (ask for group code)
    # POST:
    #   - Get group_code from form
    #   - Query groups table to find group_id
    #   - Validate group exists
    #   - Check user not already in group
    #   - Get user_id from session
    #   - INSERT into group_users table
    #   - Set session["group_id"] = group_id
    #   - If ENABLE_EMAIL_NOTIFICATIONS:
    #     - Call send_join_notification.delay(user_id, group_id)
    #     - Log event: track_event('notification.queued', {...})
    #   - Redirect to /group
    pass


@app.route("/group", methods=["GET", "POST"])
@login_required
def group():
    """Display group expenses or add new expense."""
    # TODO: Implement group page with expense addition and email notification
    # GET:
    #   - Get group_id from session
    #   - Query group name
    #   - Query all expenses in group
    #   - Render group.html with expenses list
    # POST:
    #   - Get expense_name, expense_amount from form
    #   - Validate inputs (not empty, amount is positive number)
    #   - If invalid: return apology()
    #   - Get user_id from session, group_id from session
    #   - INSERT into expenses table
    #   - Get expense_id of inserted row
    #   - If ENABLE_EMAIL_NOTIFICATIONS:
    #     - Call send_expense_notification.delay(expense_id, group_id)
    #     - Log event: track_event('notification.queued', {...})
    #   - Re-render group page with updated expenses
    pass


@app.route("/summary", methods=["GET"])
@login_required
def summary():
    """Display settlement summary for group."""
    # TODO: Implement summary with settlement notifications
    # GET:
    #   - Get group_id from session
    #   - Query all expenses in group
    #   - Query all users in group
    #   - Calculate net balances for each user
    #   - Determine settlement transactions needed
    #   - If ENABLE_EMAIL_NOTIFICATIONS:
    #     - Call send_settlement_notification.delay(transactions, group_id)
    #     - Log event: track_event('notification.queued', {...})
    #   - Render summary.html with transactions
    # 
    # Note: Complex calculation logic already exists (lines 154-218 in original)
    # Preserve existing logic, add notification call at end
    pass


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    """Display and update user notification preferences."""
    # TODO: Implement notification preferences UI
    # GET:
    #   - Get user_id from session
    #   - Query user_preferences table for this user
    #   - Render preferences.html with current settings
    #       - Checkboxes for: notify_on_join, notify_on_expense, notify_on_settlement
    #       - Current values pre-filled from database
    # POST:
    #   - Get user_id from session
    #   - Get checkbox values from form (default to False if not submitted)
    #   - UPDATE user_preferences table
    #   - Log event: track_event('notification.preference_changed', {...})
    #   - Flash message: "Preferences updated"
    #   - Redirect to preferences page
    pass


@app.route("/health/email", methods=["GET"])
def health_email():
    """Check email service health."""
    """
    Endpoint for monitoring: verify SMTP connectivity.
    
    Returns:
        JSON response with status and service info
        200: Service healthy
        503: Service unavailable
    """
    try:
        # TODO: Test email service connectivity
        # Call email_service.test_connection()
        # If successful: return {"status": "ok", "service": "email"}, 200
        # If failed: return {"status": "error", ...}, 503
        if email_service.test_connection():
            return {"status": "ok", "service": "email"}, 200
        else:
            return {"status": "error", "service": "email", "reason": "Connection failed"}, 503
    except Exception as e:
        return {"status": "error", "service": "email", "error": str(e)}, 503


@app.route("/health", methods=["GET"])
def health():
    """Overall system health check."""
    # TODO: Implement overall health check
    # Check:
    #   - Database connectivity
    #   - Email service (if ENABLE_EMAIL_NOTIFICATIONS)
    #   - Return comprehensive status
    pass


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", False))
