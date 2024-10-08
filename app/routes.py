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
