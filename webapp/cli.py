import logging
import click
from .auth.models import User, db

log = logging.getLogger(__name__)

def register(app):
    @app.cli.command('create-user')
    @click.argument('username')
    @click.argument('email')
    @click.argument('password')
    def create_user(username, email, password):
        user= User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo('User {0} Added.'.format(username))
        except Exception as e:
            log.error("Fail to add new user: %s Error: %s" 
            % (username, e))
            db.session.rollback()
    
    @app.cli.command('list-routes')
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo("%s %s %s" % (url.rule, url.methods, url.endpoint))
            