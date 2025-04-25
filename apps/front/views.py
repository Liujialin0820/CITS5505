from flask import Blueprint, views, render_template, request, session
from .forms import SignupForm, SigninForm
from utils import restful
from .models import FrontUser
from exts import db
from config import Config

bp = Blueprint("front", __name__)


@bp.route("/")
def index():
    return "front index"


class SignupView(views.MethodView):
    def get(self):
        return render_template("front/front_signin.html")

    def post(self):
        print(request.form)
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.email.data
            password = form.password1.data
            user = FrontUser(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return render_template("front/front_signup.html")

    def post(self):
        print(request.form)
        form = SigninForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session[Config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
            else:
                return restful.params_error(message="email or password is wrong.")
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
