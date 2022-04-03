from app.models import Crypto, User
from app import flask_app, db, bcrypt
from app.crypto_data import get_price, get_trending
from flask import render_template, url_for, redirect, flash, request
from app.forms import Search, Login, Register
from flask_login import login_user, current_user, logout_user


@flask_app.route('/', methods=['GET', 'POST'])
def home():
	all_tickers = Crypto.query.paginate(page=1, per_page=10, error_out=False)
	return render_template('index.html', tickers=all_tickers)


@flask_app.route('/page/<int:page_number>', methods=['GET', 'POST'])
def pagination(page_number):
	all_tickers = Crypto.query.paginate(page=page_number, per_page=10, error_out=False)
	return render_template('index.html', tickers=all_tickers)


@flask_app.route('/search', methods=['GET', 'POST'])
def searched():
	ticker_dict = {}
	ticker_list = []
	all_tickers = Crypto.query.all()
	q = request.args.get('q')
	if q:
		for ticker in all_tickers:
			if q.lower() == ticker.ticker.lower():
				ticker_list.append(ticker.cg_ticker_id)
				price = get_price(ticker.cg_ticker_id)[ticker.cg_ticker_id].get('usd')
				if price is not None:
					ticker_dict[ticker.ticker] = price
	return render_template('searched.html', all_tickers=all_tickers, ticker_dict=ticker_dict)


@flask_app.route('/trending')
def trending():
	trending_dict = get_trending()
	return render_template('trending.html', trending=trending_dict)


@flask_app.route('/buy/<ticker>', methods=['GET', 'POST'])
def buy(ticker):
	return render_template('buy.html', ticker=ticker)


@flask_app.route('/sell/<ticker>', methods=['GET', 'POST'])
def sell(ticker):
	return render_template('sell.html', ticker=ticker)


@flask_app.route('/portfolio')
def portfolio():
	return render_template('portfolio.html')


@flask_app.route('/register', methods=['GET', 'POST'])
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


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	login_form = Login()
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, login_form.password.data):
			login_user(user, remember=login_form.remember.data)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check your credentials')
	return render_template('login.html', login_form=login_form)


@flask_app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))