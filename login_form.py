from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired('username is null')])
    password = PasswordField('password', validators=[DataRequired('password is null')])
