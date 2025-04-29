# encoding: utf-8

from ..common.forms import BaseForm
from wtforms.validators import Regexp, EqualTo, Email, InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class SignupForm(BaseForm):
    username = StringField(
        validators=[
            Regexp(
                r".{2,20}", message="Please enter a valid username (2-20 characters)."
            )
        ]
    )
    email = StringField(validators=[Email(), InputRequired()])
    password1 = StringField(
        validators=[
            Regexp(
                r"[0-9a-zA-Z_\.]{6,20}",
                message="Please enter a valid password (6-20 characters).",
            )
        ]
    )
    stu_id = StringField(
        validators=[
            Regexp(
                r"[0-9a-zA-Z_\.]{6,20}",
                message="Please enter a valid student id (6-20 characters).",
            )
        ]
    )
    password2 = StringField(
        validators=[EqualTo("password1", message="Passwords do not match.")]
    )


class SigninForm(BaseForm):
    email = StringField(validators=[Email(), InputRequired()])
    password = StringField(
        validators=[
            Regexp(
                r"[0-9a-zA-Z_\.]{6,20}",
                message="Please enter a valid password (6-20 characters).",
            )
        ]
    )
    remember = StringField()

class EnrollmentForm(FlaskForm):
    user_id = StringField(validators=[DataRequired()])
    timeslot_id = IntegerField(validators=[DataRequired()])