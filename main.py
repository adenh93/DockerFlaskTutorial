from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func
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

tags = db.Table('post_tags', 
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')), 
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')) 
) 

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

def sidebar_data():
  recent = Post.query.order_by(Post.created_date.desc()).limit(5).all()
  top_tags = db.session.query(
    Tag, func.count(tags.c.post_id).label('total')
  ).join(tags).group_by(Tag).limit(5).all()

  return recent, top_tags

@app.route('/')
@app.route('/<int:page>')
def home(page=1):
  posts = Post.query.order_by(Post.created_date.desc()).paginate(page, app.config.get('POSTS_PER_PAGE', 10), False)
  recent, top_tags = sidebar_data()
  return render_template(
    'home.html',
    posts=posts,
    recent=recent,
    top_tags=top_tags
  )

@app.route('/post/<int:post_id>')
def post(post_id):
  post = Post.query.get_or_404(post_id)
  recent, top_tags = sidebar_data()
  return render_template(
    'post.html',
    post=post,
    recent=recent,
    top_tags=top_tags
  )

@app.route('/posts_by_tag/<string:tag_name>')
def posts_by_tag(tag_name):
  tag = Tag.query.filter_by(title=tag_name).first_or_404()
  posts = tag.posts.order_by(Post.created_date.desc()).all()
  recent, top_tags = sidebar_data()
  return render_template(
    'tag.html',
    tag=tag,
    posts=posts,
    recent=recent,
    top_tags=top_tags
  )

@app.route('/posts_by_user/<string:username>')
def posts_by_user(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = user.posts.order_by(Post.created_date.desc()).all()
  recent, top_tags = sidebar_data()
  return render_template(
    'user.html',
    user=user,
    posts=posts,
    recent=recent,
    top_tags=top_tags
  )

if __name__ == '__main__':
    app.run()