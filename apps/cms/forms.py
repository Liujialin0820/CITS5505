from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo, NumberRange
from ..common.forms import BaseForm
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField(validators=[Email(), InputRequired()])
    password = StringField(validators=[Length(6, 20)])
    remember = IntegerField()


class RegisterForm(Form):
    username = StringField(validators=[InputRequired(message="Username required")])
    email = StringField(validators=[Email(message="Invalid email"), InputRequired()])
    password = StringField(
        validators=[Length(6, 20, message="Password must be 6-20 characters")]
    )
    confirm_password = StringField(
        validators=[EqualTo("password", message="Passwords must match")]
    )
    security_code = StringField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20)])
    newpwd = StringField(validators=[Length(6, 20)])
    newpwd2 = StringField(validators=[EqualTo("newpwd")])


class AddcourseForm(BaseForm):
    name = StringField(validators=[InputRequired()])


class UpdatecourseForm(AddcourseForm):
    course_id = IntegerField(validators=[InputRequired()])


class AddTimeslotForm(FlaskForm):
    course_id = IntegerField(validators=[DataRequired()])
    day_of_week = IntegerField(validators=[DataRequired(), NumberRange(0, 6)])  # 0=Monday, 6=Sunday
    start_hour = IntegerField(validators=[DataRequired(), NumberRange(0, 23)])
    duration_hours = IntegerField(validators=[DataRequired(), NumberRange(1, 24)])


class UpdateTimeslotForm(FlaskForm):
    timeslot_id = IntegerField(validators=[DataRequired()])
    day_of_week = IntegerField(validators=[DataRequired(), NumberRange(0, 6)])
    start_hour = IntegerField(validators=[DataRequired(), NumberRange(0, 23)])
    duration_hours = IntegerField(validators=[DataRequired(), NumberRange(1, 24)])