from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired('username is null')])
    email = StringField('email', validators=[DataRequired('email is null')])
    password = PasswordField('password', validators=[DataRequired('password is null')])
    en_password = PasswordField('en_password', validators=[DataRequired('en_password is null')])
    code = StringField('code', validators=[DataRequired('code is null')])
