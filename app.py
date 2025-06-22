from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # настройка дб: указали относительный путь 
db = SQLAlchemy(app) # инициализировали базу данных  

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Task {self.id}>"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # если поступает новая задача
        task_content = request.form["content"] # в index.html создана input с name = "content" 
        new_task = ToDo(content=task_content) # преобразуем в модель
        try:
            db.session.add(new_task) # добавляем новую задачу
            db.session.commit() 
            return redirect('/') # перезагружаем страницу
        except:
            return "Error 404" # появилась какая-то ошибка при добавлении дела, вывели ошибку
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all() # список всех дел
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task = ToDo.query.get_or_404(id)
    try: 
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "Error 404, problem with deleting"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = ToDo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form["update"] # так как в update.html создана input с name == "update"
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error 404"
    
    else:
        return render_template('update.html', task=task)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)     