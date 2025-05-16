from flask import session, redirect, url_for  # Import Flask session handling and redirect utilities
from functools import wraps  # Import wraps to preserve metadata of the original function
from config import Config  # Import configuration settings (e.g., session key names)

def login_required(func):
    # This is a decorator that restricts access to authenticated users only.

    @wraps(func)  # Preserve original function's metadata (like __name__, __doc__)
    def inner(*args, **kwargs):
        # Inner function that will replace the decorated function
        if Config.FRONT_USER_ID in session:
            # If the user session contains a valid FRONT_USER_ID,
            # the user is considered logged in, so allow the function to run.
            return func(*args, **kwargs)
        else:
            # If the session does not contain the required ID,
            # redirect the user to the sign-in page.
            return redirect(url_for("front.signin"))

    return inner  # Return the inner function to be used as the decorated version
