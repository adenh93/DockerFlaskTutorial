from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func
from flask_migrate import Migrate
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from config import DevConfig
import timeago
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

class CommentForm(Form):
  name = StringField(
    'Name',
    validators=[DataRequired(), Length(max=255)]
  )
  title = StringField(
    'Title',
    validators=[DataRequired(), Length(max=255)]
  )
  body = TextAreaField(
    'Comment',
    validators=[DataRequired()]
  )


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

class Post(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  body = db.Column(db.Text())
  created_date = db.Column(db.DateTime(), default=datetime.now)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
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

blog_blueprint = Blueprint(
  'blog',
  __name__,
  template_folder='templates/blog',
  url_prefix="/blog"
)

@app.route('/')
def index():
  return redirect(url_for('blog.home'))

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
  posts = Post.query.order_by(Post.created_date.desc()).paginate(page, app.config.get('POSTS_PER_PAGE', 15), False)
  return render_template(
    'home.html',
    posts=posts
  )

@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
  form = CommentForm()
  if form.validate_on_submit():
    comment = Comment()
    comment.name = form.name.data
    comment.title = form.title.data
    comment.body = form.body.data
    comment.post_id = post_id
    try:
      db.session.add(comment)  
      db.session.commit()
    except Exception as e:
      flash('Error adding comment %s' % str(e), 'error')
      db.session.rollback()
    else:
      flash('Comment added successfully', 'info')
    return redirect(url_for('blog.post', post_id=post_id))

  post = Post.query.get_or_404(post_id)
  comments = post.comments.order_by(Comment.created_date.desc()).all()
  return render_template(
    'post.html',
    post=post,
    comments=comments,
    timeago=timeago,
    form=form
  )

@blog_blueprint.route('/posts_by_tag/<string:tag_name>')
def posts_by_tag(tag_name):
  tag = Tag.query.filter_by(title=tag_name).first_or_404()
  posts = tag.posts.order_by(Post.created_date.desc()).all()
  return render_template(
    'tag.html',
    tag=tag,
    posts=posts
  )

@blog_blueprint.route('/posts_by_user/<string:username>')
def posts_by_user(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = user.posts.order_by(Post.created_date.desc()).all()
  return render_template(
    'user.html',
    user=user,
    posts=posts
  )

@app.errorhandler(404)
def page_not_found(error):
  return render_template('blog/404.html'), 404

app.register_blueprint(blog_blueprint)

if __name__ == '__main__':
    app.run()