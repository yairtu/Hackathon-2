import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = "AHF34bdiujfh1809hlkjf487aj4"
	SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'accounts.db') }"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
