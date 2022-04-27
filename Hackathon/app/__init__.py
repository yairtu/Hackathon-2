from flask import Flask
import flask_migrate
import flask_sqlalchemy

from app.config import Config

from flask_bcrypt import Bcrypt
from pycoingecko import CoinGeckoAPI
from flask_login import LoginManager

cg = CoinGeckoAPI()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()


def create_app():
	flask_app = Flask(__name__)
	flask_app.config.from_object(Config)

	db.init_app(flask_app)
	migrate.init_app(flask_app, db, render_as_batch=True)
	bcrypt.init_app(flask_app)
	login_manager.init_app(flask_app)

	from app import routes, error_handlers, models
	from app.crypto_data import get_price

	from app.main.routes import main
	from app.user.routes import user
	from app.error_handlers.routes import error_handlers
	flask_app.register_blueprint(main)
	flask_app.register_blueprint(user)
	flask_app.register_blueprint(error_handlers)

	flask_app.jinja_env.globals.update(get_price=get_price)
	return flask_app
