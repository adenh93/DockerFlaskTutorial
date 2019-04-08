from . import bcrypt, AnonymousUserMixin
from .. import db


class User(db.Model): 
    id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(255), nullable=False, index=True, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True) 
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username, name, email):
        self.username = username
        self.name = name
        self.email = email

    @property
    def is_authenticated(self):
        return not isinstance(self, AnonymousUserMixin)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

