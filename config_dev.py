import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    LP_GROUP_NAME='Leominster Philosophy Group'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///app.db'
    SECRET_KEY = 'Iwonttellyou'
    LP_ADMIN = 'admin@her.abode'
    LP_MAIL_SUBJECT_PREFIX = '[Leominster Philosophers]'
    LP_MAIL_SENDER ='Phil Leominster <leominsterphil@gmail.com>' 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PASSWORD='eolo xotp gxib hdki'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass

