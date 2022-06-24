from os import path, getenv

from dotenv import dotenv_values

dotenv_path = path.join(path.dirname(__file__), '.env')
config = dotenv_values(dotenv_path)


class Config(object):
    ENV = 'development'
    DEBUG = False
    TESTING = False
    LOGIN = config.get("DB_USERNAME")
    PASSWORD = config.get("DB_PASSWORD")
    PORT = config.get("PORT", 5432)
    DB_NAME = config.get("DB_NAME", "blog")

    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv(
        "SQLALCHEMY_DATABASE_URI",
        f'postgresql+pg8000://{LOGIN}:{PASSWORD}@localhost:{PORT}/{DB_NAME}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
