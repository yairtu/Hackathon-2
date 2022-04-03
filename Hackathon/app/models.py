from app import db
from datetime import datetime
from app import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(20), unique=True, nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Crypto(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ticker = db.Column(db.String(20))
	cg_ticker_id = db.Column(db.String(20))
	name = db.Column(db.String(20))
	market_cap = db.Column(db.Float(40))
