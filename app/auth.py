from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .models import User, db

auth = Blueprint('auth', __name__)

# Route for serving login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')  # Ensure you have this template

#Route for serving logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 