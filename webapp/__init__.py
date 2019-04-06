from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(error):
    return render_template('blog/404.html'), 404


def create_app(object_name):
    from .blog.controllers import blog_blueprint
    from .main.controllers import main_blueprint

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_error_handler(404, page_not_found)
    return app