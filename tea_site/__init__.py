from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_heroku import Heroku
from celery import Celery
from tea_site.config import Config, ProdConfig

db = SQLAlchemy()
heroku = Heroku()
celery = Celery(__name__, broker=ProdConfig.CELERY_BROKER_URL)
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "alert alert-info"


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app
    heroku.init_app(app)
    login_manager.init_app(app)

    celery.conf.update(app.config)

    from tea_site.main.routes import main
    from tea_site.users.routes import users
    from tea_site.testing.routes import testing
    from tea_site.stats.routes import stats

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(testing)
    app.register_blueprint(stats)

    return app
