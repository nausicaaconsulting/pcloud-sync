import zoneinfo

from environs import Env

env = Env()
env.read_env()

CONFIG_FILE = '../../config.json'

# ADMIN
ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SECRET_KEY = env.str('SECRET_KEY')

ADMIN_LOGIN = env.str('ADMIN_LOGIN')
ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
