from app import db
from datetime import datetime


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(20), unique=True)
	username = db.Column(db.String(20), unique=True)
	created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Crypto(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ticker = db.Column(db.String(20))