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
from .forms import SignupForm, SigninForm, PreferenceForm
from utils import restful
from .models import FrontUser
from exts import db
from config import Config
from apps.common.models import CourseModel
from .decorators import login_required
from sqlalchemy import or_
from .forms import PreferenceForm
from .models import PreferenceModel,Enrollment
from apps.front.models import Message  # 确保你有这个模型
from ..common.models import CourseModel, WeeklyTimeSlot
from datetime import datetime

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


@bp.route("/message/")
@login_required
def message_page():
    user_id = session.get(Config.FRONT_USER_ID)
    return render_template("front/message.html", current_user_id=user_id)


@bp.route("/api/users")
@login_required
def get_users():
    current_user_id = session.get(Config.FRONT_USER_ID)
    users = FrontUser.query.filter(FrontUser.id != current_user_id).all()
    return restful.success(
        data={"users": [{"id": u.id, "username": u.username} for u in users]}
    )


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
        message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)

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
        user_id = session.get(Config.FRONT_USER_ID)
        course_data = Enrollment.get_user_enrollments_with_times(user_id)
        print(course_data)
        return render_template("front/time_table.html", courses=course_data)


@bp.route('/add_enrollment/', methods=['POST'])
@login_required
def add_enrollment():
    course_id = request.form.get('new_course')
    user_id = session.get(Config.FRONT_USER_ID)

    if not user_id:
        return jsonify({'code': 401, 'message': '用户未登录'}), 401
    if not course_id:
        return jsonify({'code': 400, 'message': '请选择一个课程'}), 400

    course = CourseModel.query.get(course_id)
    if not course:
        return jsonify({'code': 404, 'message': '课程不存在'}), 404

    # 可选：检查是否已选该课程，防止重复选课
    exists = Enrollment.query.filter_by(user_id=user_id, course_id=course.id).first()
    if exists:
        return jsonify({'code': 409, 'message': '您已选择该课程'}), 409

    # 不绑定 timeslot
    enrollment = Enrollment(
        user_id=user_id,
        course_id=course.id
        # timeslot_id=None，省略
    )
    db.session.add(enrollment)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'数据库错误：{e}'}), 500

    return jsonify({'code': 200, 'message': '选课成功'}), 200

@bp.route('/remove_enrollment/', methods=['POST'])
@login_required
def remove_enrollment():
    data = request.get_json()
    course_ids = data.get('course_ids')
    user_id = session.get(Config.FRONT_USER_ID)

    if not user_id:
        return jsonify({'code': 401, 'message': 'User not logged in'}), 401
    if not course_ids:
        return jsonify({'code': 400, 'message': 'No course IDs provided'}), 400

    try:
        # 删除对应课程的 Enrollment 记录
        Enrollment.query.filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id.in_(course_ids)
        ).delete(synchronize_session=False)

        db.session.commit()
        return jsonify({'code': 200, 'message': 'Enrollment(s) removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'Database error: {e}'}), 500
    
@bp.route('/my_courses/', methods=['GET'])
@login_required
def view_my_courses():
    user_id = session.get(Config.FRONT_USER_ID)
    if not user_id:
        return jsonify({'code': 401, 'message': 'User not logged in'}), 401

    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    course_list = []

    for enrollment in enrollments:
        course = CourseModel.query.get(enrollment.course_id)
        if not course:
            continue

        # 取 enrollment 里关联的 timeslot（学生实际选的）
        ts = enrollment.timeslot
        if ts:
            timeslot_info = {
                'day_of_week': ts.day_of_week,        # 0=Monday
                'start_hour': ts.start_hour,          # e.g., 10 for 10am
                'duration_hours': ts.duration_hours   # e.g., 2 hours
            }
        else:
            timeslot_info = None

        course_list.append({
            'course_id': course.id,
            'course_name': course.name,
            'timeslot': timeslot_info
        })

    # 如果前端 loadCourses() 按照 “纯数组” 来处理，就直接返回列表
    return jsonify(course_list), 200

# 获取课程时间段
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

# 修改已选课程的时间段
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


class PreferenceView(views.MethodView):
    decorators = [login_required]

    def get(self):
        course_data = CourseModel.get_all_courses_with_times()

        return render_template(
            "front/preference.html",
            courses=course_data,
        )


bp.add_url_rule("/signup/", view_func=SignupView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SigninView.as_view("signin"))
bp.add_url_rule("/timetable/", view_func=TimetableView.as_view("timetable"))
bp.add_url_rule("/preference/", view_func=PreferenceView.as_view("preference"))
