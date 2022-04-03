from app.models import Crypto, User
from app import flask_app, db, bcrypt
import json
from app.crypto_data import get_price, get_trending
from flask import render_template, url_for, redirect, flash
from app.forms import Search, Login, Register
import time


def validate_search(form):
	q = form.search.data
	return redirect(url_for('searched', q=q))


@flask_app.route('/', methods=['GET', 'POST'])
def home():
	form = Search()
	if form.validate_on_submit():
		return validate_search(form)
	all_tickers = Crypto.query.paginate(page=1, per_page=10, error_out=False)
	return render_template('index.html', tickers=all_tickers, form=form)


@flask_app.route('/page/<int:page_number>', methods=['GET', 'POST'])
def pagination(page_number):
	all_tickers = Crypto.query.paginate(page=page_number, per_page=10, error_out=False)
	form = Search()
	if form.validate_on_submit():
		return validate_search(form)
	return render_template('index.html', tickers=all_tickers, form=form)


@flask_app.route('/search/<q>', methods=['GET', 'POST'])
def searched(q):
	ticker_dict = {}
	ticker_list = []
	form = Search()
	if form.validate_on_submit():
		return validate_search(form)
	all_tickers = Crypto.query.all()
	for ticker in all_tickers:
		if q.lower() == ticker.ticker.lower():
			ticker_list.append(ticker.cg_ticker_id)
			price = get_price(ticker.cg_ticker_id)[ticker.cg_ticker_id].get('usd')
			if price is not None:
				ticker_dict[ticker.ticker] = price
	return render_template('searched.html', q=q, all_tickers=all_tickers, ticker_dict=ticker_dict, form=form)


@flask_app.route('/trending')
def trending():
	form = Search()
	trending_dict = get_trending()
	if form.validate_on_submit():
		return validate_search(form)
	return render_template('trending.html', form=form, trending=trending_dict)


@flask_app.route('/buy/<ticker>', methods=['GET', 'POST'])
def buy(ticker):
	form = Search()
	if form.validate_on_submit():
		return validate_search(form)
	return render_template('buy.html', form=form, ticker=ticker)


@flask_app.route('/sell/<ticker>', methods=['GET', 'POST'])
def sell(ticker):
	form = Search()
	if form.validate_on_submit():
		return validate_search(form)
	return render_template('sell.html', form=form, ticker=ticker)


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
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
	login_form = Login()
	return render_template('login.html', login_form=login_form)
