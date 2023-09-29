import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flaskext.markdown import Markdown
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import config as config

bootstrap = Bootstrap5()
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Some safe defaults for the (development) server to use
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI= 'sqlite:///app.db',
        SECURITY_PASSWORD_SALT ="very-important"
    )

    if test_config == 'testing':
        app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        LP_ADMIN='administrator@example.com',
        TESTING = True ) 
    else:
        app.config.from_object(config.Config)

    #print('config: ',app.config)

    bcrypt = Bcrypt(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    bootstrap.init_app(app)
    mail.init_app(app)
    
    Markdown(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .helpf import helpf as helpf_blueprint
    app.register_blueprint(helpf_blueprint, url_prefix='/helpf')

    return app
