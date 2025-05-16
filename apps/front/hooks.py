from config import Config  # Import configuration constants (e.g., session key names)
from flask import session, g  # Import session for accessing user session data, g for storing global request variables
from .models import FrontUser  # Import the user model from the current app
from .views import bp  # Import the Flask Blueprint object

@bp.before_request
def before_request():
    # This function runs before every request handled by the 'bp' blueprint.
    # It checks whether the user is logged in based on the session.

    if Config.FRONT_USER_ID in session:
        # If the session contains a user ID (i.e., user is logged in),
        user_id = session.get(Config.FRONT_USER_ID)  # Retrieve the user ID from the session
        user = FrontUser.query.get(user_id)  # Query the database to get the user object by ID
        if user:
            g.user = user  # Store the user object in Flask's 'g' context for use during this request
