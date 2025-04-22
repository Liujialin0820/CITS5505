from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo


class LoginForm(Form):
    email = StringField(validators=[Email(), InputRequired()])
    password = StringField(validators=[Length(6, 20)])
    remember = IntegerField()


class RegisterForm(Form):
    username = StringField(validators=[InputRequired(message="Username required")])
    email = StringField(validators=[Email(message="Invalid email"), InputRequired()])
    password = StringField(
        validators=[Length(6, 20, message="Password must be 6–20 characters")]
    )
    confirm_password = StringField(
        validators=[EqualTo("password", message="Passwords must match")]
    )
