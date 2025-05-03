from flask import Blueprint, views, render_template, request, session, redirect, url_for
from .forms import SignupForm, SigninForm
from utils import restful
from .models import FrontUser
from exts import db
from config import Config
from apps.common.models import CourseModel
from .decorators import login_required
from sqlalchemy import or_
from apps.front.models import Message  # 确保你有这个模型

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

@bp.route("/message/")
@login_required
def message_page():
    return render_template("front/message.html")

@bp.route("/api/users")
@login_required
def get_users():
    current_user_id = session.get(Config.FRONT_USER_ID)
    users = FrontUser.query.filter(FrontUser.id != current_user_id).all()
    return restful.success(data={"users": [{"id": u.id, "username": u.username} for u in users]})

@bp.route("/api/messages")
@login_required
def get_messages():
    current_user_id = session.get(Config.FRONT_USER_ID)
    target_id = request.args.get("with")
    messages = Message.query.filter(
        or_(
            (Message.sender_id == current_user_id) & (Message.receiver_id == target_id),
            (Message.sender_id == target_id) & (Message.receiver_id == current_user_id),
        )
    ).order_by(Message.timestamp.asc()).all()

    return restful.success(data={
        "messages": [
            {"sender": m.sender.username, "content": m.content}
            for m in messages
        ]
    })

@bp.route("/api/send_message", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    content = data.get("content")
    receiver_id = data.get("receiver_id")
    sender_id = session.get(Config.FRONT_USER_ID)

    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()
    return restful.success()


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
