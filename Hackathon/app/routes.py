from app.models import Crypto, User, Trade, Portfolio
from app import flask_app, db, bcrypt
from app.crypto_data import get_price, get_trending
from flask import render_template, url_for, redirect, flash, request
from app.forms import Login, Register, BuyForm, SellForm
from flask_login import login_user, current_user, logout_user, login_required


@flask_app.route('/crypto', methods=['GET', 'POST'])
def crypto():
	all_tickers = Crypto.query.paginate(page=1, per_page=10, error_out=False)
	return render_template('index.html', tickers=all_tickers)


@flask_app.route('/crypto/page/<int:page_number>', methods=['GET', 'POST'])
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
				price = get_price(ticker.cg_ticker_id)
				if price is not None:
					ticker_dict[ticker.ticker] = price
	return render_template('searched.html', all_tickers=all_tickers, ticker_dict=ticker_dict)


@flask_app.route('/trending')
def trending():
	trending_dict = get_trending()
	return render_template('trending.html', trending=trending_dict)


@flask_app.route('/buy/<ticker>', methods=['GET', 'POST'])
@login_required
def buy(ticker):
	form = BuyForm()
	crypto = Crypto.query.filter_by(ticker=ticker).first()
	current_usd = current_user.usd
	price = float(get_price(crypto.cg_ticker_id))
	holding_amount = current_holding_amount(crypto.id)
	holding_value = value(price=price, quantity=holding_amount)
	max_buy_amount = current_usd / price
	if form.validate_on_submit():
		if max_buy_amount < form.amount.data:
			flash(f"You cannot exceed the maximum buy amount", "danger")
			return redirect(url_for('buy', ticker=ticker))
		else:
			trade = Trade(quantity=form.amount.data, current_price=price, crypto=crypto, user=current_user, buy=True)
			user_portfolio = current_user.portfolio
			for item in user_portfolio:
				if int(item.crypto_id) == crypto.id:
					item.quantity += trade.quantity
					db.session.add(trade)
					db.session.commit()
					return redirect(url_for('portfolio'))
			portfolio = Portfolio(crypto_id=crypto.id, ticker=crypto.ticker,
								  quantity=form.amount.data, user_portfolio=current_user)
			db.session.add(portfolio)
			db.session.commit()
			current_user.usd = current_user.usd - (price * form.amount.data)
			db.session.add(trade)
			db.session.commit()
			return redirect(url_for('portfolio'))
	return render_template('buy.html', crypto=crypto, value=holding_value, holding=holding_amount,
						   max_buy_amount=max_buy_amount, form=form, price=price)


@flask_app.route('/sell/<ticker>', methods=['GET', 'POST'])
@login_required
def sell(ticker):
	form = SellForm()
	crypto = Crypto.query.filter_by(ticker=ticker).first()
	price = float(get_price(crypto.cg_ticker_id))
	holding_amount = current_holding_amount(crypto.id)
	holding_value = value(price=price, quantity=holding_amount)
	if form.validate_on_submit():
		if holding_amount < form.amount.data:
			flash(f"Your sell amount cannot exceed your holding quantity", "danger")
			return redirect(url_for('sell', ticker=ticker))
		else:
			trade = Trade(quantity=form.amount.data, current_price=price, crypto=crypto, user=current_user, buy=False)
			current_user.usd += price * form.amount.data
			user_portfolio = current_user.portfolio
			for item in user_portfolio:
				if int(item.crypto_id) == crypto.id:
					item.quantity -= trade.quantity
			db.session.add(trade)
			db.session.commit()
			return redirect(url_for('portfolio'))
	return render_template('sell.html', crypto=crypto, value=holding_value, holding=holding_amount,
						   form=form, price=price)


@flask_app.route('/portfolio')
@login_required
def portfolio():
	portfolio_data = []
	portfolio = current_user.portfolio
	total_holding_value = 0
	for item in portfolio:
		crypto = Crypto.query.filter_by(id=item.crypto_id).first()
		price = get_price(crypto.cg_ticker_id)
		current_holding_value = value(price=float(price), quantity=item.quantity)
		portfolio_data.append(
			{'ticker': crypto.ticker,
			 'price': price,
			 'holding_amount': item.quantity,
			 'current_holding_value': current_holding_value
			 }
		)
		total_holding_value += current_holding_value
	percent_change = (total_holding_value + current_user.usd - 10000) / 100
	return render_template('portfolio.html', portfolio=portfolio_data, percent_change=percent_change)


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
			redir_page = request.args.get('next')
			return redirect(redir_page) if redir_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check your credentials', 'danger')
	return render_template('login.html', login_form=login_form)


@flask_app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@flask_app.route('/')
@flask_app.route('/start_trading')
def home():
	return render_template('start_trading.html')


def current_holding_amount(crypto_id):
	user_portfolio = current_user.portfolio
	for item in user_portfolio:
		if int(item.crypto_id) == crypto_id:
			return item.quantity
	return 0


def value(price: float, quantity: float):
	return price * quantity
