from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_course_table = db.Table(
    "user_course",
    db.Column("user_id", db.Integer, db.ForeignKey("front_user.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course_model.id")),
)


class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    username = db.Column(db.String(50), nullable=False)
    stu_id = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    enrollments = db.relationship(
        "Enrollment", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get("password")
            kwargs.pop("password")
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)


class Enrollment(db.Model):
    __tablename__ = "enrollment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id", name="fk_enrollment_course_id"),
        nullable=False,
    )
    timeslot_id = db.Column(
        db.Integer, db.ForeignKey("weekly_timeslot.id"), nullable=True
    )

    enroll_time = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("FrontUser", back_populates="enrollments")
    course = db.relationship("CourseModel")  # optional: backref="enrollments"
    timeslot = db.relationship("WeeklyTimeSlot", back_populates="enrollments")


    @staticmethod
    def get_user_enrollments_with_times(user_id):
        """
        返回该 user_id 的所有 enrollment 记录，
        每条记录包含：course_id, course_name, timeslot 或 None
        """
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        result = []
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for en in enrollments:
            course = en.course
            # 如果 enrollment.timeslot_id 为空，则 timeslot 为 None
            ts = en.timeslot
            if ts:
                timeslot_info = [{
                    "day_of_week": ts.day_of_week,
                    "start_hour": ts.start_hour,
                    "duration_hours": ts.duration_hours,
                    # 可选：给前端直接好用的字符串
                    "label": f"{days[ts.day_of_week]} {ts.start_hour}:00 ({ts.duration_hours}h)"
                }]
            else:
                timeslot_info = None

            result.append({
                "course_id": course.id,
                "course_name": course.name,
                "timeslots": timeslot_info
            })

        return result
    
    
class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(
        db.String(100), db.ForeignKey("front_user.id"), nullable=False
    )
    receiver_id = db.Column(
        db.String(100), db.ForeignKey("front_user.id"), nullable=False
    )
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship(
        "FrontUser", foreign_keys=[sender_id], backref="sent_messages"
    )
    receiver = db.relationship(
        "FrontUser", foreign_keys=[receiver_id], backref="received_messages"
    )


class PreferenceModel(db.Model):
    __tablename__ = "course_model"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
