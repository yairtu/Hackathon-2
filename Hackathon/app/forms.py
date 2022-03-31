from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length


class Search(FlaskForm):
	search = StringField("Search for ticker")
	submit = SubmitField('Submit')