from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError,Length
from app import db
import sqlalchemy as sa 
from app.models import User


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(max=50, message="Maximum 50")])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=40, message="Maximum 40")])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    

class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(max=50, message="Maximum 50")])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=40, message="Maximum 40")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_login(self, login):
        query = sa.select(User).where(User.login == login.data)
        user = db.session.scalar(query)
        if user is not None:
            raise ValidationError
        