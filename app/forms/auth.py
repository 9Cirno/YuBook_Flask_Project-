from wtforms import Form, StringField, IntegerField,PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(4, 64), Email(message="bad email given")])

    password = PasswordField(validators=[DataRequired(message='password can not be empty'), Length(8, 64)])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message = "atleast 2 chars max 10 chars")])


    def validate_email(self, field):
        #db.session
        if User.query.filter_by(email=field.data).first():
            raise (ValidationError('email is used'))


    def validate_nickname(self, field):
        #db.session
        if User.query.filter_by(nickname=field.data).first():
            raise (ValidationError('name is used'))


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="bad email given")])

    password = PasswordField(validators=[DataRequired(message='password can not be empty'), Length(8, 64)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(4, 64), Email(message="bad email given")])


class ResetPasswordForm(Form):
    a =1
    password1 = PasswordField(validators=[
        DataRequired('password can not be empty'),
        Length(8, 64),
        EqualTo('password2', message="2 password entered are different")
    ])

    password2 = PasswordField([
        DataRequired('password can not be empty'),
        Length(8, 64)
    ])
