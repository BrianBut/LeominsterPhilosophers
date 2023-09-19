import os
basedir = os.path.abspath(os.path.dirname(__file__))

#This config is for testing
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    LP_MAIL_SUBJECT_PREFIX = '[Phil Leominster]'
    LP_MAIL_SENDER = 'Phil Leominster <leominsterphil@proton.me>'
    LP_ADMIN = os.environ.get('LP_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    @staticmethod
    def init_app(app):
        pass

