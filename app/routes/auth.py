from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.extensions import db
from app.forms.auth import LoginForm, RegisterForm

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        existing_user =  User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))
        
        new_user = User(username = username, email = email, is_admin = False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form = form)

@auth_bp.route('/login',methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email = email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('admin.dashboard' if user.is_admin else "user.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template("login.html", form = form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.", "info")
    return redirect(url_for('auth.login'))

#Code ends here