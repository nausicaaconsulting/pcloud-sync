import zoneinfo

from environs import Env

env = Env()
env.read_env()

# ADMIN
ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
# Connect to signals to get notified before and after changes are committed to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
ADMIN_LOGIN = env.str('ADMIN_LOGIN')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
