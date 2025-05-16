from exts import db  # Import the SQLAlchemy database instance
import shortuuid  # Used to generate short unique IDs
from werkzeug.security import generate_password_hash, check_password_hash  # For password encryption and verification
from datetime import datetime  # For timestamp fields

# Association table for many-to-many relation between users and courses (not used directly in the model)
user_course_table = db.Table(
    "user_course",
    db.Column("user_id", db.Integer, db.ForeignKey("front_user.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course_model.id")),
)


class FrontUser(db.Model):
    # User model representing users in the frontend system
    __tablename__ = "front_user"

    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)  # Primary key with short UUID
    username = db.Column(db.String(50), nullable=False)  # Display name of the user
    stu_id = db.Column(db.String(50), nullable=False)  # Student identifier
    _password = db.Column(db.String(100), nullable=False)  # Encrypted password (private field)
    email = db.Column(db.String(50), unique=True, nullable=False)  # Unique email address
    join_time = db.Column(db.DateTime, default=datetime.now)  # Time the user registered

    enrollments = db.relationship(
        "Enrollment", back_populates="user", cascade="all, delete-orphan"
    )  # One-to-many relationship with Enrollment

    def __init__(self, *args, **kwargs):
        # Override constructor to allow setting raw password during user creation
        if "password" in kwargs:
            self.password = kwargs.get("password")  # Will trigger password setter
            kwargs.pop("password")  # Remove raw password from kwargs before calling super
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        # Getter for the password (returns hashed password)
        return self._password

    @password.setter
    def password(self, newpwd):
        # Automatically hash the password before storing
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        # Verifies a raw password against the stored hashed password
        return check_password_hash(self._password, rawpwd)


class Enrollment(db.Model):
    # Table representing a user's enrollment in a course with an optional time slot
    __tablename__ = "enrollment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"), nullable=False)  # Link to the user
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id", name="fk_enrollment_course_id"),
        nullable=False,
    )  # Link to course (foreign key constraint explicitly named)
    timeslot_id = db.Column(
        db.Integer, db.ForeignKey("weekly_timeslot.id"), nullable=True
    )  # Optional link to a scheduled timeslot

    enroll_time = db.Column(db.DateTime, default=datetime.now)  # Time of enrollment

    user = db.relationship("FrontUser", back_populates="enrollments")  # Reverse relation to FrontUser
    course = db.relationship("CourseModel")  # Relationship to course (can be made bidirectional)
    timeslot = db.relationship("WeeklyTimeSlot", back_populates="enrollments")  # Reverse relation from timeslot

    @staticmethod
    def get_user_enrollments_with_times(user_id):
        """
        Returns all enrollments for the given user_id.
        Each record includes course_id, course_name, and optional timeslot info.
        This is used for frontend display of the user's selected schedule.
        """
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        result = []
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # Used for formatting timeslot labels

        for en in enrollments:
            course = en.course  # Access linked course object
            ts = en.timeslot  # Access linked timeslot, if exists
            if ts:
                # Timeslot info is available
                timeslot_info = [{
                    "day_of_week": ts.day_of_week,
                    "start_hour": ts.start_hour,
                    "duration_hours": ts.duration_hours,
                    "label": f"{days[ts.day_of_week]} {ts.start_hour}:00 ({ts.duration_hours}h)"
                }]
            else:
                # No timeslot assigned yet
                timeslot_info = None

            result.append({
                "course_id": course.id,
                "course_name": course.name,
                "timeslots": timeslot_info
            })

        return result


class Message(db.Model):
    # Represents a message exchanged between users (direct messaging system)
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key

    sender_id = db.Column(
        db.String(100), db.ForeignKey("front_user.id"), nullable=False
    )  # ID of sender (foreign key to user)
    receiver_id = db.Column(
        db.String(100), db.ForeignKey("front_user.id"), nullable=False
    )  # ID of receiver (foreign key to user)
    content = db.Column(db.Text, nullable=False)  # Message body content
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when message was sent

    sender = db.relationship(
        "FrontUser", foreign_keys=[sender_id], backref="sent_messages"
    )  # Relationship to sender user
    receiver = db.relationship(
        "FrontUser", foreign_keys=[receiver_id], backref="received_messages"
    )  # Relationship to receiver user


class PreferenceModel(db.Model):
    # Represents available course choices (for scheduling preferences)
    __tablename__ = "course_model"
    id = db.Column(db.Integer, primary_key=True)  # Unique course ID
    code = db.Column(db.String(100), unique=True, nullable=False)  # Unique course code (e.g., CITS5505)
    name = db.Column(db.String(100), nullable=False)  # Human-readable course name (e.g., "Database Systems")
