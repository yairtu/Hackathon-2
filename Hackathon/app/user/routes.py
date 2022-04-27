from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user

from app import bcrypt, db
from app.forms import Register, Login
from app.models import User

user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	registration_form = Register()
	if registration_form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(registration_form.password.data).decode("utf-8")
		user = User(email=registration_form.email.data,
					username=registration_form.username.data,
					password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f"Account for {registration_form.username.data}", "success")
		return redirect(url_for('login'))
	return render_template('register.html', registration_form=registration_form)


@user.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	login_form = Login()
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, login_form.password.data):
			login_user(user, remember=login_form.remember.data)
			redir_page = request.args.get('next')
			return redirect(redir_page) if redir_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check your credentials', 'danger')
	return render_template('login.html', login_form=login_form)


@user.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@user.route('/')
@user.route('/start_trading')
def home():
	return render_template('start_trading.html')