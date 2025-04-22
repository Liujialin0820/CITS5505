from config import Config
from flask import session,g
from .models import CMSUser
from .views import bp


@bp.before_request
def before_request():
    if Config.CMS_USER_ID in session:
        user_id = session.get(Config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user
