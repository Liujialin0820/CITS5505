from flask import session, redirect, url_for
from functools import wraps
from config import Config


def login_required(func):

    @wraps(func)
    def inner(*args, **kwargs):
        if Config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))

    return inner
