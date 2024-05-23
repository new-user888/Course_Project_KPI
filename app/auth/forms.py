from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.auth.models import User


def user_exists(form, field):
    user = User.query.filter_by(user_name=field.data).first()
    if user:
        raise ValidationError('User with this username already exists')


class RegistrationForm(FlaskForm):
    name = StringField('Enter your new username',
                       validators=[DataRequired(), Length(3, 20, message='3-20 symbols are required'), user_exists])
    about = StringField('Tell something about you', validators=[DataRequired(), Length(0, 100, message='100 symbols are allowed')])
    private = StringField('Something private (Only confirmed person will see this information)',
                          validators=[DataRequired(), Length(0, 100, message='100 symbols are allowed')])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 20, message="password should contain 6-20 symbols"),
                                         EqualTo('confirm')])
    confirm = PasswordField('Confirm', validators=[DataRequired(), Length(6, 20, message="password should contain 6-20 symbols")])
    submit = SubmitField('Register dating profile!')


class LoginForm(FlaskForm):
    name = StringField('Enter your username',
                       validators=[DataRequired(), Length(3, 20, message='3-20 symbols are required')])
    password = PasswordField('Enter your password', validators=[DataRequired()])
    stay_logged_in = BooleanField('Stay logged-in')
    submit = SubmitField('Login')
