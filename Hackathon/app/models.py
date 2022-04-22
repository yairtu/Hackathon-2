from cryptocompare import get_price

from app import db
from datetime import datetime
from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# users_trades = db.Table(
# 	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
# 	db.Column('trade_id', db.Integer, db.ForeignKey('trade.id')),
# )


# users_cryptos = db.Table('users_cryptos',
# 						 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
# 						 db.Column('crypto_id', db.Integer, db.ForeignKey('crypto.id')),
# 						 )


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(20), unique=True, nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	usd = db.Column(db.Float, default=10000.0)
	# cryptos = db.relationship('Crypto', secondary='users_cryptos', backref='user_cryptos')
	trades = db.relationship('Trade', backref='user')
	# user_trades = db.relationship('Trade', secondary=users_trades, backref='user_trades')
	portfolio = db.relationship('Portfolio', backref='user_portfolio')


class Crypto(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ticker = db.Column(db.String(20))
	cg_ticker_id = db.Column(db.String(20))
	name = db.Column(db.String(20))
	market_cap = db.Column(db.Float(40))
	trade = db.relationship('Trade', backref='crypto')


class Trade(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	trade_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	quantity = db.Column(db.Float, nullable=False)
	current_price = db.Column(db.Float)
	crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	buy = db.Column(db.Boolean, nullable=False)


class Portfolio(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	crypto_id = db.Column(db.Integer)
	ticker = db.Column(db.String(10))
	quantity = db.Column(db.Float, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))