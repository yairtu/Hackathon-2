from flask import Flask
import flask_migrate
import flask_sqlalchemy

from app.config import Config

from flask_bcrypt import Bcrypt
from pycoingecko import CoinGeckoAPI
from flask_login import LoginManager

cg = CoinGeckoAPI()

flask_app = Flask(__name__)

bcrypt = Bcrypt(flask_app)
login_manager = LoginManager(flask_app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
flask_app.config.from_object(Config)
db = flask_sqlalchemy.SQLAlchemy(flask_app)
migrate = flask_migrate.Migrate(flask_app, db, render_as_batch=True)

from app import routes, error_handlers, models
from app.crypto_data import get_price

flask_app.jinja_env.globals.update(get_price=get_price)

db.create_all()
