import flask
from app import flask_app


@flask_app.errorhandler(404)
def error_404(error):
	return flask.render_template('404_error.html'), 404


@flask_app.errorhandler(429)
def error_429(error):
	return flask.render_template('440_error.html'), 429
