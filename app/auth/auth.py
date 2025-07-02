from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

import sqlalchemy as sa

from .forms import LoginForm, RegistrationForm

from app.models import User, Category
from app import db


auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth')

@login_required
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.login == form.login.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login or password")
            return redirect(url_for('auth_bp.login'))
                        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home_bp.index')
        return redirect(next_page)       
        
    return render_template('login.html', form=form)

@login_required
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


@auth_bp.route('/register', methods=['POST', 'GET'])
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
            return redirect(url_for('auth_bp.login'))

        except:
            return "Error 404..."
        
        

    return render_template('register.html', form=form)


