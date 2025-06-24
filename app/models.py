import sqlalchemy as sa  
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, List


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model): 
    """Модель пользователя
        наследуемся от UserMixin, чтобы были безопасно реализованы 4 обязательные элемента 
        для flask_login: is_authenticated, is_activate, is_anonymous, get_id()
    """    
    __tablename__ = 'users'
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    login: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False, unique=True)
    hashed_password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    tasks: so.Mapped[List["Task"]] = so.relationship(back_populates="user")
    
    categories: so.Mapped[List["Category"]] = so.relationship(back_populates="user")
    
    def __repr__(self):
        return f"<{self.id}: User {self.login}>"  
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    type_category: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), nullable=False)
    
    user: so.Mapped[User] = so.relationship(back_populates="categories")
    
    tasks: so.Mapped[List["Task"]] = so.relationship(back_populates="category")
        
    def __repr__(self):
        return f"{self.type_category}"


class Task(db.Model): 
    """Модель задачи
    Используется отношение один ко многим: 
    У одного пользователя может быть несколько задач
    Также используется двусторонняя связь. По задаче можно определить к какому пользователю она относится
    """
    __tablename__ = 'tasks'
       
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    content: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)
    
    date_created: so.Mapped[datetime] = so.mapped_column(sa.DateTime(), default= datetime.now() )
    
    deadline: so.Mapped[Optional[date]] = so.mapped_column(sa.Date())

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"), nullable=False) # внешний ключ
    
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("categories.id"), nullable=False) # внешний ключ
        
    user: so.Mapped[User] = so.relationship(back_populates="tasks")    
    
    category: so.Mapped[Category] = so.relationship(back_populates="tasks")
    
    def __repr__(self):
        return f"<Task {self.id}>"