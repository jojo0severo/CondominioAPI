import os
import secrets
import redis
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = secrets.token_urlsafe(30)
    DEBUG = False
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2)


class DevelopmentConfig(BaseConfig):
    # redis_password = os.environ.get('REDIS_PASSWORD')
    # redis_db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=redis_password)

    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/data/api.db'
    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = redis_db

    SUPER_USER_URL = 'secret'


class ProductionConfig(BaseConfig):
    db_url = os.environ.get('DATABASE_URL') or 'UnknownDatabase'

    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{db_url[11:]}'

    SUPER_USER_URL = secrets.token_urlsafe(44)

