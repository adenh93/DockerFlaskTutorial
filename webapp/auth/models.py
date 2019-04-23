from . import bcrypt, AnonymousUserMixin
from .. import db

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model): 
    id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(255), nullable=False, index=True, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True) 
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username, email):
        self.username = username
        self.email = email
        default = Role.query.filter_by(name="blogposter").one()
        self.roles.append(default)
        
    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
            return False

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


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name


