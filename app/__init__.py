from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from config import Config
from flask_migrate import Migrate
from sqlalchemy import MetaData

import sqlalchemy as sa

convention = {
"ix": 'ix_%(column_0_label)s',
"uq": "uq_%(table_name)s_%(column_0_name)s",
"ck": "ck_%(table_name)s_%(constraint_name)s",
"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
"pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth_bp.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    # db = SQLAlchemy(app, metadata=metadata) # инициализировали базу данных  
    # migrate = Migrate(app, db, render_as_batch=True) # инициализация миграции базы данных
    
    db.init_app(app=app)
    migrate.init_app(app=app, db=db, render_as_batch=True)
    login.init_app(app)
    
    from app.auth.auth import auth_bp
    from app.main.main import main_bp
    from app.home.home import home_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(home_bp)
    
    return app






# app = Flask(__name__)
# app.config.from_object(Config) # настройка приложения

# login = LoginManager(app) # инициализировали flask_login
# login.login_view = 'login'

# convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)

# db = SQLAlchemy(app, metadata=metadata) # инициализировали базу данных  
# migrate = Migrate(app, db, render_as_batch=True) # инициализация миграции базы данных


# # BluePrints

# from app_blueprints.auth.auth import auth_bp
# from app_blueprints.home.home import home_bp
# from app_blueprints.main.main import main_bp


# app.register_blueprint(auth_bp)
# app.register_blueprint(home_bp)
# app.register_blueprint(main_bp)

    

# from app import routes, models