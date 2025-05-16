# encoding: utf-8
# This file defines form validation logic for user sign-up and sign-in using WTForms.

from ..common.forms import BaseForm  # Import a custom base form class (possibly adds common behavior or styling)
from wtforms.validators import Regexp, EqualTo, Email, InputRequired  # Import standard WTForms validators
from wtforms import StringField  # Import text field type for forms


class SignupForm(BaseForm):
    # This form is used for user registration. It validates inputs such as username, email, password, and student ID.

    username = StringField(
        validators=[
            Regexp(
                r".{2,20}",  # Matches any string with 2 to 20 characters
                message="Please enter a valid username (2-20 characters)."  # Custom error message if validation fails
            )
        ]
    )

    email = StringField(
        validators=[
            Email(),  # Ensures the input is in a valid email format
            InputRequired()  # Ensures the field is not empty
        ]
    )

    password1 = StringField(
        validators=[
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z_\.]{6,20}$",  # Requires at least one lowercase, one uppercase, 6-20 valid characters
                message="Password must be 6-20 characters and include both uppercase and lowercase letters."  # Error message if pattern doesn't match
            )
        ]
    )

    stu_id = StringField(
        validators=[
            Regexp(
                r"[0-9a-zA-Z_\.]{6,20}",  # Accepts alphanumeric, underscore, and dot, between 6-20 characters
                message="Please enter a valid student id (6-20 characters)."  # Error message if validation fails
            )
        ]
    )

    password2 = StringField(
        validators=[
            EqualTo("password1", message="Passwords do not match.")  # Ensures both password fields match
        ]
    )


class SigninForm(BaseForm):
    # This form is used for user login. It validates email and password inputs.

    email = StringField(
        validators=[
            Email(),  # Checks email format
            InputRequired()  # Field must be filled
        ]
    )

    password = StringField(
        validators=[
            Regexp(
                r"[0-9a-zA-Z_\.]{6,20}",  # Checks for 6-20 characters with valid set
                message="Please enter a valid password (6-20 characters)."  # Shown on validation failure
            )
        ]
    )

    remember = StringField()  # Optional field to support "remember me" functionality (no validators)