from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
import flask_login


class LoginUser(flask_login.UserMixin):
    def __init__(self, username, password=None, phone_number=None):
        self.username = username
        self.password = password
        self.phone_sms_code = phone_number

    def login(self):
        flask_login.login_user(self.username)


class LoginFormStepOne(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_sms_code = IntegerField('Phone SMS Code', validators=[DataRequired(), Length(5)])
    submit = SubmitField('Oturum Aç')


class LoginFormStepTwo(FlaskForm):
    phone_sms_code = IntegerField('Phone SMS Code', validators=[DataRequired(), Length(5)])
    submit = SubmitField('Kodu Gönder')
