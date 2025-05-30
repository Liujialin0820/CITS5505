# encoding: utf-8

from ..common.forms import BaseForm
from wtforms.validators import Regexp, EqualTo, Email, InputRequired
from wtforms import StringField


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
                r"^(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_\.]{6,20}$",
                message="Password must be 6-20 characters and include both uppercase and lowercase letters.",
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

