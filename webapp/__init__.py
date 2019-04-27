from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_celery import Celery
from flask_caching import Cache
from flask_assets import Environment, Bundle

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
celery = Celery()
cache = Cache()
assets_env = Environment()

main_css = Bundle(
    'css/bootstrap.min.css',
    'css/font-awesome.css',
    'css/site-style.css',
    'css/site-style.css',
    filters='cssmin',
    output='css/common.css'
)

main_js = Bundle(
    'js/jquery-3.3.1.slim.min.js',
    'js/popper.min.js',
    'js/bootstrap.min.js',
    filters='jsmin',
    output='js/common.js'
)

def page_not_found(error):
    return render_template('404.html'), 404


def create_app(object_name):
    from .blog.controllers import blog_blueprint
    from .main.controllers import main_blueprint

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    celery.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    from .auth import create_module as auth_create_module
    from .blog import create_module as blog_create_module
    from .main import create_module as main_create_module
    from .api import create_module as api_create_module
    auth_create_module(app)
    blog_create_module(app)
    main_create_module(app)
    api_create_module(app)
    app.register_error_handler(404, page_not_found)
    assets_env.register("main_js", main_js)
    assets_env.register("main_css", main_css)
    
    return app