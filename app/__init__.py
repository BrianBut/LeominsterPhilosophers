from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flaskext.markdown import Markdown
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#import config_production as config
import config_development as config
#import config_testing as config

bootstrap = Bootstrap5()
mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.Config)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
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
