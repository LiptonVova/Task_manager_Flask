from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Optional, Length
from app import db
import sqlalchemy as sa 
from app.models import User, Category
from flask_login import current_user
from flask import flash


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
        
        
class TaskForm(FlaskForm):
    content = StringField('Description', validators=[DataRequired(), Length(max = 200, message="Maximum 200")])
    category = SelectField('Category')
    deadline = DateField('Deadline', validators=[Optional()])
    submit = SubmitField('Add task')
    
    
class CategoryForm(FlaskForm):
    category = StringField('Type', validators=[DataRequired(), Length(max=50, message="Maximum 50")])
    submit = SubmitField('Add category')
    
    def validate_category(self, category):
        query = sa.select(Category).where(sa.and_(
            Category.type_category == category.data, Category.user_id == current_user.id
        ))
        current_category = db.session.scalar(query)
        if current_category is not None:
            flash("Такая категория уже есть")
            raise ValidationError
    

class DeleteCategoryForm(FlaskForm):
    category = SelectField('Type')
    submit = SubmitField('Delete category')