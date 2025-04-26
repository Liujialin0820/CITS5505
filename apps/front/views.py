from flask import Blueprint, views, render_template, request, session, redirect, url_for
from .forms import SignupForm, SigninForm
from utils import restful
from .models import FrontUser
from exts import db
from config import Config
from apps.common.models import CourseModel
from .decorators import login_required

bp = Blueprint("front", __name__)


@bp.route("/")
@login_required
def index():
    courses = CourseModel.query.all()
    context = {
        "courses": courses,
    }
    return render_template("front/front_dashboard.html", **context)


@bp.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("front.signin"))


class SignupView(views.MethodView):
    def get(self):
        return render_template("front/front_signup.html")

    def post(self):
        print(request.form)
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            stu_id = form.stu_id.data
            user = FrontUser(
                email=email, username=username, password=password, stu_id=stu_id
            )
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class SigninView(views.MethodView):
    def get(self):
        return render_template("front/front_signin.html")

    def post(self):
        print(request.form)
        form = SigninForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session[Config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
            else:
                return restful.params_error(message="email or password is wrong.")
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class TimetableView(views.MethodView):
    def get(self):
        return render_template("front/time_table.html")


class PreferenceView(views.MethodView):
    def get(self):
        return render_template("front/preference.html")


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
bp.add_url_rule("/timetable/", view_func=TimetableView.as_view("timetable"))
bp.add_url_rule("/preference/", view_func=PreferenceView.as_view("preference"))
