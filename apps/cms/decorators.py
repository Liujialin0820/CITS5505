from flask import session, redirect, url_for  # Import session handling and redirection utilities from Flask
from functools import wraps  # Import wraps to preserve metadata of the original function when decorating
from config import Config  # Import application-wide config (e.g. session keys)

def login_required(func):
    # Custom decorator to restrict access to authenticated CMS users only

    @wraps(func)  # Ensures the decorated function retains its original name and docstring
    def inner(*args, **kwargs):
        # Inner function that will be called in place of the original function

        if Config.CMS_USER_ID in session:
            # If CMS user is logged in (user ID exists in session), proceed with the original function
            return func(*args, **kwargs)
        else:
            # If not logged in, redirect to the CMS login page
            return redirect(url_for("cms.login"))

    return inner  # Return the wrapped version of the original function
