from config import Config  # Import global configuration constants (e.g. session key names)
from flask import session, g  # Import session for user tracking and g for global request context
from .models import CMSUser  # Import the CMS user model
from .views import bp  # Import the CMS blueprint instance

@bp.before_request
def before_request():
    # This function runs before every request handled by the 'cms' blueprint.
    # It checks whether the CMS user is logged in by verifying the session.
    
    if Config.CMS_USER_ID in session:
        # If the user ID is found in session, retrieve it
        user_id = session.get(Config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)  # Fetch the CMS user from the database
        
        if user:
            g.cms_user = user  # Attach the user object to Flask's global context for this request

