from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config) # настройка приложения

login = LoginManager(app) # инициализировали flask_login
login.login_view = 'login'

db = SQLAlchemy(app) # инициализировали базу данных  
migrate = Migrate(app, db) # инициализация миграции базы данных

from app import routes, models