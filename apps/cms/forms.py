from wtforms import Form, StringField, IntegerField  # Basic form and field types
from wtforms.validators import Email, InputRequired, Length, EqualTo, NumberRange  # Built-in validators
from ..common.forms import BaseForm  # Custom base form with utility methods
from flask_wtf import FlaskForm  # Flask-integrated version of WTForms Form
from wtforms.validators import DataRequired  # Similar to InputRequired, ensures field has value

# Login form for CMS user authentication
class LoginForm(Form):
    email = StringField(validators=[Email(), InputRequired()])  # Required, valid email
    password = StringField(validators=[Length(6, 20)])  # Password must be 6–20 characters
    remember = IntegerField()  # Optional flag for “remember me” checkbox

# Registration form for CMS admin users
class RegisterForm(Form):
    username = StringField(validators=[InputRequired(message="Username required")])  # Username must be provided
    email = StringField(validators=[Email(message="Invalid email"), InputRequired()])  # Valid and required email
    password = StringField(
        validators=[Length(6, 20, message="Password must be 6-20 characters")]  # Password length check
    )
    confirm_password = StringField(
        validators=[EqualTo("password", message="Passwords must match")]  # Must match the above password
    )
    security_code = StringField()  # Security code required for registration (compared to Config.SECRET_KEY)

# Form for resetting an admin password
class ResetpwdForm(BaseForm):  # Inherits utility from BaseForm (e.g., get_error)
    oldpwd = StringField(validators=[Length(6, 20)])  # Old password
    newpwd = StringField(validators=[Length(6, 20)])  # New password
    newpwd2 = StringField(validators=[EqualTo("newpwd")])  # Must match new password

# Form to create a new course (used by admin panel)
class AddcourseForm(BaseForm):
    name = StringField(validators=[InputRequired()])  # Name of the new course

# Form to update a course; extends AddcourseForm by including course ID
class UpdatecourseForm(AddcourseForm):
    course_id = IntegerField(validators=[InputRequired()])  # ID of course to update

# Form to add a new timeslot for a course
class AddTimeslotForm(FlaskForm):
    course_id = IntegerField(validators=[DataRequired()])  # Target course ID
    day_of_week = IntegerField(validators=[DataRequired(), NumberRange(0, 6)])  # 0 = Monday, 6 = Sunday
    start_hour = IntegerField(validators=[DataRequired(), NumberRange(0, 23)])  # Start time in 24h format
    duration_hours = IntegerField(validators=[DataRequired(), NumberRange(1, 24)])  # Duration in hours

# Form to update an existing timeslot
class UpdateTimeslotForm(FlaskForm):
    timeslot_id = IntegerField(validators=[DataRequired()])  # ID of timeslot to update
    day_of_week = IntegerField(validators=[DataRequired(), NumberRange(0, 6)])  # New day of week
    start_hour = IntegerField(validators=[DataRequired(), NumberRange(0, 23)])  # New start time
    duration_hours = IntegerField(validators=[DataRequired(), NumberRange(1, 24)])  # New duration
