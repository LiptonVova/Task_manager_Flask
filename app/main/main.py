from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user

import sqlalchemy as sa

from app import db
from app.models import Category, Task
from .forms import TaskForm, CategoryForm, DeleteCategoryForm

from datetime import datetime

main_bp = Blueprint('main_bp', __name__, template_folder="../templates/main")

@login_required
@main_bp.route('/add', methods=['POST', 'GET'])
def new_task():
    form = TaskForm()
    
    query = sa.select(Category).where(Category.user == current_user)    
    categories = [category for category in db.session.scalars(query)]   
    form.category.choices = categories
    
    if form.validate_on_submit():
        newTask = Task()
        
        newTask.content = form.content.data
        newTask.deadline = form.deadline.data
        query = sa.select(Category).where(Category.type_category == form.category.data)
        newTask.category= db.session.scalar(query)
        newTask.user = current_user
        
        try:        
            db.session.add(newTask)
            db.session.commit()
                       
            return redirect(url_for('home_bp.index'))
            
        except:
            return "Error 404..."
            
    return render_template('add_task.html', form=form)

@login_required
@main_bp.route('/add_category', methods=['POST', 'GET'])
def add_category():
    form = CategoryForm()
    

    if form.validate_on_submit():
        new_category = Category(type_category=form.category.data)
        new_category.user = current_user
        
        try:
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('home_bp.index'))
        except:
            return "Error 404..."
    
    return render_template('add_category.html', form=form)

@login_required
@main_bp.route('/delete_category', methods=['POST', 'GET'])
def delete_category():
    form = DeleteCategoryForm()
    
    # показываем все категории, кроме дефолтной. В нашей случае это категория "Без категории"
    query = sa.select(Category).where(Category.user_id == current_user.id)
    all_categories = db.session.scalars(query)
    current_categories = [category for category in all_categories if category.type_category != "Без категории"]
    form.category.choices = current_categories
        
    if form.validate_on_submit():
        query = sa.select(Category).where(sa.and_(
                (Category.type_category == form.category.data), 
                Category.user_id == current_user.id)
            ) # находим выбранную категорию у текущего пользователя
        
        category = db.session.scalar(query)
        
        query = sa.select(Task).where(Task.category_id == category.id)
        tasks = db.session.scalars(query).all() # задачи, у которых была категория, которую удаляем
        
        # у всех задач, у которых была удаляемая категория, заменяем ее на дефолтную
        if (len(tasks) > 0):
            flash(
                "Внимание, вы удалили категорию, которая была использована в каких то задачах,\
                она была заменена на 'Без категории' ")
            query = sa.select(Category).where(sa.and_(
                Category.user_id == current_user.id, Category.type_category == "Без категории"
            ))
            
            default_category = db.session.scalar(query)
            
            for task in tasks:
                task.category = default_category
                task.category_id = default_category.id
                               
        try:
            db.session.delete(category)
            db.session.commit()
            
            return redirect(url_for('home_bp.index'))        
    
        except:
            return "Error 404..."
    
    return render_template('delete_category.html', form=form, current_categories=current_categories)


@login_required
@main_bp.route('/edit_task/<int:id>', methods=['POST', 'GET'])
def edit_task(id):
    form = TaskForm()
    
    query = sa.select(Task).where(Task.id == id)
    currentTask = db.session.scalar(query)
    
    query = sa.select(Category).where(Category.user_id == current_user.id)
    categories = db.session.scalars(query).all()
    form.category.choices = categories
    
    if currentTask is None:
        return f"Error 404...Task {id} is not exist" 
    
    if form.validate_on_submit():
        currentTask.content = form.content.data
        currentTask.date_created = datetime.now()
        currentTask.deadline = form.deadline.data
        query = sa.select(Category).where(Category.type_category == form.category.data)
        currentTask.category = db.session.scalar(query)
        
        try:
            db.session.add(currentTask)
            db.session.commit()
            
            return redirect(url_for('home_bp.index'))
            
        except:
            return "Error 404"
        
    elif request.method == "GET":
        form.category.data = currentTask.category.type_category
        form.content.data = currentTask.content
        form.deadline.data = currentTask.deadline
           
    return render_template("edit_task.html", form=form)        


@login_required
@main_bp.route('/delete/<int:id>')
def delete(id):
    query = sa.select(Task).where(Task.id == id)
    task = db.session.scalar(query)
    try: 
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error 404, problem with deleting"
