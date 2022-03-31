from flask import Flask
import flask_migrate
import flask_sqlalchemy

from app.config import Config

from flask_bcrypt import Bcrypt
import cryptocompare

flask_app = Flask(__name__)

flask_app.config.from_object(Config)
bcrypt = Bcrypt(flask_app)

db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)

from app import routes, error_handlers, models


def get_price(ticker):
	return cryptocompare.get_price(ticker, currency='USD')


flask_app.jinja_env.globals.update(get_price=get_price)

db.create_all()
