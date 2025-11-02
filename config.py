import os

class Config:
    DB_USER_ENV = 'DB_USER'
    DB_PASSWORD_ENV = 'DB_PASSWORD'
    DB_HOST_ENV = 'DB_HOST'
    DB_NAME_ENV = 'DB_NAME'

    SQLALCHEMY_DATABASE_URI = None # Este valor será sobrescrito en create_app o por TestConfig

    SQLALCHEMY_TRACK_MODIFICATIONS = False