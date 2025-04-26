from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify,
)
from .forms import (
    LoginForm,
    RegisterForm,
    ResetpwdForm,
    AddcourseForm,
    UpdatecourseForm,
    AddTimeslotForm,
    UpdateTimeslotForm,
)
from .models import CMSUser
from exts import db
from .decorators import login_required
from config import Config
from utils import restful
from apps.common.models import CourseModel, WeeklyTimeSlot


bp = Blueprint("cms", __name__, url_prefix="/cms")


@bp.route("/logout/")
@login_required
def logout():
    del session[Config.CMS_USER_ID]
    return redirect(url_for("cms.login"))


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/login.html", message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[Config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for("cms.courses"))
            else:
                return self.get(message="email or password error")
        else:
            message = form.errors.popitem()[0] + ": " + form.errors.popitem()[1][0]
            return self.get(message=message)


class RegisterView(views.MethodView):
    def get(self, message=None):
        return render_template("cms/register.html", message=message)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            security_code = form.security_code.data

            if security_code != Config.SECRET_KEY:
                message = "Security code error. Please contact the administrator."
                return self.get(message=message)

            # check if already registered
            existing_user = CMSUser.query.filter_by(email=email).first()
            if existing_user:
                return self.get(message="Email already registered")

            # create new user
            user = CMSUser(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("cms.login"))
        else:
            field, errors = form.errors.popitem()
            message = f"{field}: {errors[0]}"
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("cms/cms_resetpwd.html")

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("wrong password!")
        else:
            return restful.params_error(form.get_error())


@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")


@bp.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")


@bp.route("/courses/")
@login_required
def courses():
    course_models = CourseModel.query.all()
    context = {"courses": course_models}
    return render_template("cms/cms_courses.html", **context)


@bp.route("/acourse/", methods=["POST"])
@login_required
def acourse():
    form = AddcourseForm(request.form)
    if form.validate():
        name = form.name.data
        course = CourseModel(name=name)
        db.session.add(course)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/ucourse/", methods=["POST"])
@login_required
def ucourse():
    form = UpdatecourseForm(request.form)
    if form.validate():
        course_id = form.course_id.data
        name = form.name.data
        course = CourseModel.query.get(course_id)
        if course:
            course.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route("/dcourse/", methods=["POST"])
@login_required
def dcourse():
    course_id = request.form.get("course_id")
    if not course_id:
        return restful.params_error("请传入板块id！")

    course = CourseModel.query.get(course_id)
    if not course:
        return restful.params_error(message="没有这个板块！")

    db.session.delete(course)
    db.session.commit()
    return restful.success()


@bp.route("/add_timeslot/", methods=["POST"])
@login_required
def add_timeslot():
    form = AddTimeslotForm(request.form)
    if form.validate():
        course = CourseModel.query.get(form.course_id.data)
        if not course:
            return restful.params_error("Course doesn't exist")
        try:
            course.add_weekly_timeslot(
                day_of_week=form.day_of_week.data, hour=form.hour.data
            )
            return restful.success()
        except ValueError as e:
            return restful.params_error(str(e))
    return restful.params_error(form.get_error())


@bp.route("/utimeslot/", methods=["POST"])
@login_required
def update_timeslot():
    form = UpdateTimeslotForm(request.form)
    if form.validate():
        slot = WeeklyTimeSlot.query.get(form.timeslot_id.data)
        if not slot:
            return restful.params_error("Timeslot not found")
        slot.day_of_week = form.day_of_week.data
        slot.hour = form.hour.data
        db.session.commit()
        return restful.success()
    return restful.params_error(form.get_error())


@bp.route("/dtimeslot/", methods=["POST"])
@login_required
def delete_timeslot():
    timeslot_id = request.form.get("timeslot_id")
    slot = WeeklyTimeSlot.query.get(timeslot_id)
    if not slot:
        return restful.params_error("Timeslot not found")
    db.session.delete(slot)
    db.session.commit()
    return restful.success()


bp.add_url_rule("/login/", view_func=LoginView.as_view("login"))
bp.add_url_rule("/register/", view_func=RegisterView.as_view("register"))
bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))
