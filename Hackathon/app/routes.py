from cryptocompare import cryptocompare
from app.models import Crypto
from app import flask_app, db, bcrypt
import json
from flask import render_template, url_for, redirect
from app.forms import Search


def get_price(ticker):
	return cryptocompare.get_price(ticker, currency='USD')


# def validate_search():
# 	search = Search()
# 	all_tickers = Crypto.query.all()
# 	if search.validate_on_submit():
# 		q = search.search.data
# 		ticker_list = []
# 		for t in all_tickers:
# 			if q in t:
# 				ticker_list.append(q)
# 		return redirect(url_for('searched', q=q, ticker_list=ticker_list))


@flask_app.route('/', methods=['GET', 'POST'])
def home():
	form = Search()
	if form.validate_on_submit():
		q = form.search.data
		return redirect(url_for('searched', q=q))
	all_tickers = Crypto.query.paginate(page=1, per_page=1, error_out=False)
	return render_template('index.html', tickers=all_tickers, form=form)


@flask_app.route('/search/<q>', methods=['GET', 'POST'])
def searched(q):
	ticker_dict = {}
	ticker_list = []
	error = '[ERROR] cccagg_or_exchange market does not exist for this coin pair (ETHPR-EUR)'
	all_tickers = Crypto.query.all()
	for ticker in all_tickers:
		if q in ticker.ticker:
			ticker_list.append(ticker.ticker)
			if get_price(ticker.ticker) is not None:
				ticker_dict[ticker.ticker] = get_price(ticker.ticker)[ticker.ticker]['USD']
	return render_template('searched.html', q=q, ticker_dict=ticker_dict, tickers=ticker_list, error=error)


@flask_app.route('/page/<int:page_number>', methods=['GET', 'POST'])
def pagination(page_number):
	all_tickers = Crypto.query.paginate(page=page_number, per_page=1, error_out=False)
	form = Search()
	if form.validate_on_submit():
		q = form.search.data
		return redirect(url_for('searched', q=q))
	return render_template('index.html', tickers=all_tickers, form=form)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')
