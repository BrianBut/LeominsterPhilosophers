import os
basedir = os.path.abspath(os.path.dirname(__file__))

#This config is for production
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    LP_ADMIN = os.environ.get('LP_ADMIN')
    LP_MAIL_SUBJECT_PREFIX = '[Leominster Philosophers]'
    LP_MAIL_SENDER = 'Phil Leominster <leominsterphil@gmail.com>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/brian/databases/data-prod.sqlite3'
    @staticmethod
    def init_app(app):
        pass

