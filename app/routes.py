from app import app, db
from flask import request, redirect, render_template, flash, url_for
from app.forms import LoginForm, RegistrationForm
from app.models import User, Task
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit


@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    """Начальная страница
    
    Returns:
        html - страница
    
    """
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


@app.route('/delete/<int:id>')
def delete(id):
    """Удаление задачи
     
    Args:
        id (int): id задачи

    Returns:
        html - страница
    """
    task = db.session.get(Task, id)
    try: 
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error 404, problem with deleting"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    """Редактирование задачи

    Args:
        id (int): id задачи

    Returns:
        html - страница
    """
    task = db.session.get(Task, id)
    
    if request.method == 'POST':
        task.content = request.form["update"] # так как в update.html создана input с name == "update"
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error 404"
    
    else:
        return render_template('update.html', task=task)
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.login == form.login.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login or password")
            redirect(url_for('login'))
            
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
            db.session.commit()
        
            flash("Congratulations!!! You are new user in our site!!!")
            return redirect(url_for('login'))        
        
        except:
            return "Error 404..."
        

    return render_template('register.html', form=form)