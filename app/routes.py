from flask import Blueprint

# Define the Blueprint
bp = Blueprint('main', __name__)

# Add some sample routes under the Blueprint
@bp.route('/')
def home():
    return "Welcome to the Wellness App!"

from flask import render_template, url_for, flash, redirect
from app import db, bcrypt
from app.forms import RegistrationForm
from app.models import User

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

# Wed Oct 9 login route

from flask_login import login_user, current_user, login_required, logout_user
from app.forms import LoginForm  # Ensure the LoginForm is imported

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

#logout route

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))