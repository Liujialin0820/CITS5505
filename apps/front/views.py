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
from .forms import SignupForm, SigninForm  # Import form definitions for signup and signin
from utils import restful  # Utility module for standard API responses
from .models import FrontUser  # Import user model
from exts import db  # SQLAlchemy database instance
from config import Config  # Configuration settings (e.g., session keys)
from apps.common.models import CourseModel
from .decorators import login_required  # Custom decorator to enforce login
from sqlalchemy import or_  # SQLAlchemy OR filter
from .models import Enrollment  # Import Enrollment model
from apps.front.models import Message  # Messaging model
from ..common.models import CourseModel, WeeklyTimeSlot  # Course and timeslot models
from datetime import datetime  # Timestamp utility

# Create Blueprint instance for frontend routes
bp = Blueprint("front", __name__)

# Set up user loading before each request in the app context
@bp.before_app_request
def load_user():
    user_id = session.get(Config.FRONT_USER_ID)
    if user_id:
        g.user = FrontUser.query.get(user_id)  # Attach user object to global context
    else:
        g.user = None

# Main dashboard page (requires login)
@bp.route("/")
@login_required
def index():
    user_id = session.get(Config.FRONT_USER_ID)
    courses = Enrollment.get_user_enrollments_with_times(user_id)
    context = {"courses": courses, "today": datetime.today()}
    return render_template("front/front_dashboard.html", **context)

# Log the user out and clear session
@bp.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("front.signin"))

# Message page rendering for the current user
@bp.route("/message/")
@login_required
def message_page():
    user_id = session.get(Config.FRONT_USER_ID)
    return render_template("front/message.html", current_user_id=user_id)

# API to retrieve all users except the current user
@bp.route("/api/users")
@login_required
def get_users():
    current_user_id = session.get(Config.FRONT_USER_ID)
    users = FrontUser.query.filter(FrontUser.id != current_user_id).all()
    return restful.success(
        data={"users": [{"id": u.id, "username": u.username} for u in users]}
    )

# API to retrieve messages between current user and another user
@bp.route("/api/messages")
@login_required
def get_messages():
    current_user_id = session.get(Config.FRONT_USER_ID)
    target_id = request.args.get("with")

    if not target_id:
        return restful.params_error(message="Missing target user ID.")

    try:
        messages = (
            Message.query.filter(
                or_(
                    (Message.sender_id == current_user_id)
                    & (Message.receiver_id == target_id),
                    (Message.sender_id == target_id)
                    & (Message.receiver_id == current_user_id),
                )
            )
            .order_by(Message.timestamp.asc())
            .all()
        )

        return restful.success(
            data={
                "messages": [
                    {
                        "sender": m.sender.username if m.sender else m.sender_id,
                        "content": m.content,
                        "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for m in messages
                ]
            }
        )

    except Exception as e:
        print("\u274c Error in /api/messages:", str(e))
        return restful.server_error(message="Internal error fetching messages.")

# API endpoint to send a new message
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
        message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)

        db.session.add(message)
        db.session.commit()
        print(f"\u2705 Message saved: {sender_id} -> {receiver_id}: {content}")
        return restful.success()

    except Exception as e:
        print("\u274c Exception in send_message:", e)
        return restful.server_error(message="Internal error when saving message.")

# View class for signup (GET: form, POST: register)
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

# View class for signin (GET: form, POST: login logic)
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

# View for showing a user's timetable
class TimetableView(views.MethodView):
    def get(self, uid=None):
        user_id = uid or session.get(Config.FRONT_USER_ID)
        if not user_id:
            return "\u7528\u6237\u672a\u767b\u5f55\u6216\u672a\u63d0\u4f9bUID", 400

        course_data = Enrollment.get_user_enrollments_with_times(user_id)
        return render_template("front/time_table.html", courses=course_data)

# Route to add a course enrollment for a user
@bp.route("/add_enrollment/", methods=["POST"])
@login_required
def add_enrollment():
    course_id = request.form.get("new_course")
    user_id = session.get(Config.FRONT_USER_ID)

    if not user_id:
        return jsonify({"code": 401, "message": "\u7528\u6237\u672a\u767b\u5f55"}), 401
    if not course_id:
        return jsonify({"code": 400, "message": "\u8bf7\u9009\u62e9\u4e00\u4e2a\u8bfe\u7a0b"}), 400

    course = CourseModel.query.get(course_id)
    if not course:
        return jsonify({"code": 404, "message": "\u8bfe\u7a0b\u4e0d\u5b58\u5728"}), 404

    exists = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
    if exists:
        return jsonify({"code": 409, "message": "\u60a8\u5df2\u9009\u62e9\u8be5\u8bfe\u7a0b"}), 409

    enrollment = Enrollment(
        user_id=user_id,
        course_id=course.id,
    )
    db.session.add(enrollment)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"\u6570\u636e\u5e93\u9519\u8bef\uff1a{e}"}), 500

    return jsonify({"code": 200, "message": "\u9009\u8bfe\u6210\u529f"}), 200

# Route to remove course enrollments
@bp.route("/remove_enrollment/", methods=["POST"])
@login_required
def remove_enrollment():
    data = request.get_json()
    course_ids = data.get("course_ids")
    user_id = session.get(Config.FRONT_USER_ID)

    if not user_id:
        return jsonify({"code": 401, "message": "User not logged in"}), 401
    if not course_ids:
        return jsonify({"code": 400, "message": "No course IDs provided"}), 400

    try:
        Enrollment.query.filter(
            Enrollment.user_id == user_id, Enrollment.course_id.in_(course_ids)
        ).delete(synchronize_session=False)

        db.session.commit()
        return (
            jsonify({"code": 200, "message": "Enrollment(s) removed successfully"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Database error: {e}"}), 500

# API route to get a user's current enrolled courses and timeslots
@bp.route("/my_courses/", methods=["GET"])
@login_required
def view_my_courses():
    user_id = session.get(Config.FRONT_USER_ID)
    if not user_id:
        return jsonify({"code": 401, "message": "User not logged in"}), 401

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    course_list = []

    for enrollment in enrollments:
        course = CourseModel.query.get(enrollment.course_id)
        if not course:
            continue

        ts = enrollment.timeslot
        if ts:
            timeslot_info = {
                "day_of_week": ts.day_of_week,
                "start_hour": ts.start_hour,
                "duration_hours": ts.duration_hours,
            }
        else:
            timeslot_info = None

        course_list.append(
            {
                "course_id": course.id,
                "course_name": course.name,
                "timeslot": timeslot_info,
            }
        )

    return jsonify(course_list), 200

# Return available timeslots for a given course
@bp.route("/course_timeslots/<int:course_id>/")
def course_timeslots(course_id):
    course = CourseModel.query.get(course_id)
    print(course)
    if not course:
        return jsonify({"code": 404, "message": "Course not found"})

    timeslots = [
        {
            "id": ts.id,
            "day_of_week": ts.day_of_week,
            "start_hour": ts.start_hour,
            "duration_hours": ts.duration_hours,
        }
        for ts in course.timeslots
    ]
    return jsonify({"code": 200, "timeslots": timeslots})

# Update the timeslot associated with an enrollment
@bp.route("/update_timeslot/", methods=["POST"])
def update_timeslot():
    course_id = request.form.get("course_id")
    timeslot_id = request.form.get("timeslot_id")
    user_id = session.get(Config.FRONT_USER_ID)

    enrollment = Enrollment.query.filter_by(
        user_id=user_id, course_id=course_id
    ).first()
    if not enrollment:
        return jsonify({"code": 404, "message": "Enrollment not found"})

    enrollment.timeslot_id = timeslot_id
    db.session.commit()
    return jsonify({"code": 200, "message": "Timeslot updated"})

# View for managing course preferences (course + timeslot selection UI)
class PreferenceView(views.MethodView):
    decorators = [login_required]

    def get(self):
        course_data = CourseModel.get_all_courses_with_times()

        return render_template(
            "front/preference.html",
            courses=course_data,
        )

# Register the class-based views to URL routes
bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
bp.add_url_rule("/timetable/", view_func=TimetableView.as_view("timetable"))
bp.add_url_rule("/timetable/<uid>", view_func=TimetableView.as_view("timetable_with_uid"))
bp.add_url_rule("/preference/", view_func=PreferenceView.as_view("preference"))

