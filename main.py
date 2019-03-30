from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from config import DevConfig
from datetime import datetime
 
app = Flask(__name__) 
app.config.from_object(DevConfig)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db)
migrate.init_app(app, db, render_as_batch=True)

class User(db.Model): 
  id = db.Column(db.Integer(), primary_key=True) 
  username = db.Column(db.String(255), nullable=False, index=True, unique=True) 
  password = db.Column(db.String(255))
  blogs = db.relationship(
    'Blog',
    backref='user',
    lazy='dynamic'
  ) 

class Blog(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  created_date = db.Column(db.DateTime(), default=datetime.now)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
  posts = db.relationship(
    'Post',
    backref='blog',
    lazy='dynamic'
  )

tags = db.Table('post_tags', 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')), 
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')) 
) 

class Post(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  body = db.Column(db.Text())
  created_date = db.Column(db.DateTime(), default=datetime.now)
  blog_id = db.Column(db.Integer(), db.ForeignKey('blog.id'))
  comments = db.relationship(
    'Comment',
    backref='post',
    lazy='dynamic'
  )
  tags = db.relationship(
    'Tag',
    secondary=tags,
    backref=db.backref('posts', lazy='dynamic')
  )

class Comment(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  title = db.Column(db.String(255), nullable=False)
  body = db.Column(db.Text())
  created_date = db.Column(db.DateTime(), default=datetime.now)
  post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

class Tag(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(255), nullable=False, unique=True)

  def __init__(self, title):
    self.title = title