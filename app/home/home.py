from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

import sqlalchemy as sa

from app.models import Task
from app import db 

home_bp = Blueprint('home_bp', __name__, template_folder="../templates/home")



@home_bp.route('/', methods=['POST', 'GET'])
@home_bp.route('/index', methods=['POST', 'GET'])
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
    