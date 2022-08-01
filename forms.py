from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo




class LoginForm(FlaskForm):
    username = StringField('username',
                        validators=[DataRequired(),validators.length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')