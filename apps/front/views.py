from flask import Blueprint, views, render_template, request, session, redirect, url_for, g
from .forms import SignupForm, SigninForm, PreferenceForm
from utils import restful
from .models import FrontUser
from exts import db
from config import Config
from apps.common.models import CourseModel
from .decorators import login_required
from sqlalchemy import or_
from .forms import PreferenceForm
from .models import PreferenceModel
from apps.front.models import Message  # 确保你有这个模型
from ..common.models import CourseModel  

bp = Blueprint("front", __name__)

@bp.before_app_request
def load_user():
    user_id = session.get(Config.FRONT_USER_ID)
    if user_id:
        g.user = FrontUser.query.get(user_id)
    else:
        g.user = None

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

from flask import session

from flask import request

@bp.route('/message/')
@login_required
def message_page():
    user_id =  session.get(Config.FRONT_USER_ID)
    return render_template('front/message.html', current_user_id=user_id)


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

    if not target_id:
        return restful.params_error(message="Missing target user ID.")

    try:
        messages = Message.query.filter(
            or_(
                (Message.sender_id == current_user_id) & (Message.receiver_id == target_id),
                (Message.sender_id == target_id) & (Message.receiver_id == current_user_id)
            )
        ).order_by(Message.timestamp.asc()).all()

        return restful.success(data={
            "messages": [
                {
                    "sender": m.sender.username if m.sender else m.sender_id,
                    "content": m.content,
                    "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
                for m in messages
            ]
        })

    except Exception as e:
        print("❌ Error in /api/messages:", str(e))
        return restful.server_error(message="Internal error fetching messages.")


@bp.route("/api/send_message", methods=["POST"])
@login_required
def send_message():
    if not request.is_json:
        return restful.params_error(message="Expected JSON payload.")

    data = request.get_json(silent=True)
    if not data:
        return restful.params_error(message="Invalid or empty JSON.")

    receiver_id = data.get("receiver_id")
    content = data.get("content")

    if not receiver_id or not content:
        return restful.params_error(message="Missing receiver_id or content.")

    try:
        sender_id = session.get(Config.FRONT_USER_ID)
        
        # ✅ 不要转成 int，直接作为字符串传入
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

        db.session.add(message)
        db.session.commit()
        print(f"✅ Message saved: {sender_id} -> {receiver_id}: {content}")
        return restful.success()

    except Exception as e:
        print("❌ Exception in send_message:", e)
        return restful.server_error(message="Internal error when saving message.")


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
        course_data = CourseModel.get_all_courses_with_times()
        return render_template("front/time_table.html", courses=course_data)


class PreferenceView(views.MethodView):
    decorators = [login_required]

    def get(self):
        form = PreferenceForm()
        all_courses = CourseModel.query.all()
        form.new_course.choices = [(str(c.id), c.name) for c in all_courses]

        user = g.user

        selected_ids = []
        if request.args.get("updated") == "1":
            selected_ids = [c.id for c in user.courses]

        form.courses.data = selected_ids 

        form.courses.choices = [
            (c.id, f"{c.code} - {c.name}") for c in PreferenceModel.query.all()
        ]

        return render_template(
            "front/preference.html",
            form=form,
            selected_ids=selected_ids,
            user_courses=user.courses if selected_ids else [],
            all_courses=all_courses,
            courses=PreferenceModel.query.all()
        )

    def post(self):
        form = PreferenceForm()

        # Load course options
        all_courses = CourseModel.query.all()
        form.new_course.choices = [(str(c.id), c.name) for c in all_courses]
        form.courses.choices = [
            (c.id, f"{c.code} - {c.name}") for c in PreferenceModel.query.all()
        ]

        user = g.user
        action = request.form.get("action")

        if action == "clear":
            print("clear1")
            selected_course_id = form.new_course.data
            if selected_course_id:
                print("clear2")
                base_course = CourseModel.query.get(int(selected_course_id))
                if base_course:
                    print("clear3")
                    pref = PreferenceModel.query.filter_by(name=base_course.name).first()
                    print(f"user.courses IDs = {user.courses}")
                    print(f"pref found: {pref.name} (id={pref.id})")
                    if pref and any(p.id == pref.id for p in user.courses):
                        print("clear4")
                        user.courses.remove(pref)  
                        db.session.commit()

                        #db.session.delete(pref)
                        #db.session.commit()
            return redirect(url_for("front.preference", updated=1))

        # Default: Submit preferences
        if form.validate_on_submit():
            selected_ids = form.courses.data
            selected_course_id = form.new_course.data

            if selected_course_id:
                base_course = CourseModel.query.get(int(selected_course_id))
                if base_course:
                    pref = PreferenceModel.query.filter_by(name=base_course.name).first()
                    if not pref:
                        pref = PreferenceModel(
                            code=f"AUTO-{base_course.name[:10]}",
                            name=base_course.name,
                        )
                        db.session.add(pref)
                        db.session.commit()
                    selected_ids.append(pref.id)
                    user.courses.append(pref)

            user.courses = PreferenceModel.query.filter(
                PreferenceModel.id.in_(selected_ids)
            ).all()
            db.session.commit()
            return redirect(url_for("front.preference", updated=1))

        return "Form validation failed", 400


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
bp.add_url_rule("/timetable/", view_func=TimetableView.as_view("timetable"))
bp.add_url_rule("/preference/", view_func=PreferenceView.as_view("preference"))
