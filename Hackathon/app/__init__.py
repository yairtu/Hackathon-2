import jinja2
from flask import Flask
import flask_migrate
import flask_sqlalchemy
from jinja2 import filters

from app.config import Config

from flask_bcrypt import Bcrypt
from pycoingecko import CoinGeckoAPI
from flask_login import LoginManager

cg = CoinGeckoAPI()

flask_app = Flask(__name__)

flask_app.config.from_object(Config)
bcrypt = Bcrypt(flask_app)
login_manager = LoginManager(flask_app)
db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db)


def get_price(ticker_id):
	return cg.get_price(ticker_id, vs_currencies='usd')[ticker_id].get('usd')


flask_app.jinja_env.globals.update(get_price=get_price)

from app import routes, error_handlers, models

db.create_all()
