from config import Config
from flask import session, g
from .models import FrontUser
from .views import bp


@bp.before_request
def before_request():
    if Config.FRONT_USER_ID in session:
        user_id = session.get(Config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        if user:
            g.user = user
