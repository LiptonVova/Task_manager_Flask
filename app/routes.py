from app import app, db
from flask import request, redirect, render_template, flash, url_for
from app.forms import LoginForm, RegistrationForm, TaskForm, CategoryForm, DeleteCategoryForm
from app.models import User, Task, Category
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from datetime import datetime


@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST': # если поступает новая задача
        task_content = request.form["content"] # в index.html создана input с name = "content" 
        new_task = Task(content=task_content, user=current_user) # преобразуем в модель
        try:
            db.session.add(new_task) # добавляем новую задачу
            db.session.commit() 
            return redirect('/') # перезагружаем страницу
        except:
            return "Error 404" # появилась какая-то ошибка при добавлении дела, вывели ошибку
    else:
        query = sa.select(Task).where(Task.user == current_user).order_by(Task.date_created)
        tasks = db.session.scalars(query).all() # список всех дел
        return render_template('index.html', tasks=tasks)


@login_required
@app.route('/add', methods=['POST', 'GET'])
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
                       
            return redirect(url_for('index'))
            
        except:
            return "Error 404..."
            
    return render_template('add_task.html', form=form)

@login_required
@app.route('/add_category', methods=['POST', 'GET'])
def add_category():
    form = CategoryForm()
    

    if form.validate_on_submit():
        new_category = Category(type_category=form.category.data)
        new_category.user = current_user
        
        try:
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Error 404..."
    
    return render_template('add_category.html', form=form)

@login_required
@app.route('/delete_category', methods=['POST', 'GET'])
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
            
            return redirect(url_for('index'))        
    
        except:
            return "Error 404..."
    
    return render_template('delete_category.html', form=form, current_categories=current_categories)


@login_required
@app.route('/edit_task/<int:id>', methods=['POST', 'GET'])
def edit_task(id):
    form = TaskForm()
    
    query = sa.select(Task).where(Task.id == id)
    currentTask = db.session.scalar(query)
    
    query = sa.select(Category).where(User.id == current_user.id)
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
            
            return redirect(url_for('index'))
            
        except:
            return "Error 404"
        
    elif request.method == "GET":
        form.category.data = currentTask.category.type_category
        form.content.data = currentTask.content
        form.deadline.data = currentTask.deadline
           
    return render_template("edit_task.html", form=form)        


@login_required
@app.route('/delete/<int:id>')
def delete(id):
    query = sa.select(Task).where(Task.id == id)
    task = db.session.scalar(query)
    try: 
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error 404, problem with deleting"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.login == form.login.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login or password")
            return redirect(url_for('login'))
                        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)       
        
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data)
        user.set_password(password=form.password.data)
        
        try:
            db.session.add(user)        
        
        except:
            return "Error 404..."
        
        
        # нужно найти в базе данных найти нового пользователя, чтобы подтянулся user_id
        query = sa.select(User).where(User.login == user.login)
        cur_user = db.session.scalar(query)
        
        default_category = Category(type_category="Без категории", user=cur_user)
        # за каждым пользователем закреплена как минимум одна категория ("Без категории")
        
        try:
            db.session.add(default_category)
            db.session.commit()

            flash("Congratulations!!! You are new user in our site!!!")
            return redirect(url_for('login'))

        except:
            return "Error 404..."
        
        

    return render_template('register.html', form=form)