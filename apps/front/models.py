from exts import db
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime

user_course_table = db.Table(
    "user_course",
    db.Column("user_id", db.Integer, db.ForeignKey("front_user.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course_model.id"))
)

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    username = db.Column(db.String(50), nullable=False)
    stu_id = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)
    courses = db.relationship(
        "PreferenceModel",  # ← apps.common.models
        secondary=user_course_table,
        backref="students"
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
    timeslot_id = db.Column(db.Integer, db.ForeignKey("weekly_timeslot.id"), nullable=False)
    enroll_time = db.Column(db.DateTime, default=datetime.now)

    # back-populates
    # user = db.relationship("FrontUser", back_populates="enrollments")
    timeslot = db.relationship("WeeklyTimeSlot", back_populates="enrollments")

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    receiver_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship("FrontUser", foreign_keys=[sender_id], backref="sent_messages")
    receiver = db.relationship("FrontUser", foreign_keys=[receiver_id], backref="received_messages")

class PreferenceModel(db.Model):
    __tablename__ = "course_model"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)