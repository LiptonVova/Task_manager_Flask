from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Optional, Length
from flask_login import current_user

import sqlalchemy as sa

from app.models import Category
from app import db

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