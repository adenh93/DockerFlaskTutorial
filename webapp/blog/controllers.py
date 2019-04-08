from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from .models import db, Post, Tag, Comment
from ..auth.models import User
from .forms import CommentForm
import timeago

blog_blueprint = Blueprint(
  'blog',
  __name__,
  template_folder='../templates/blog',
  static_folder='../../static',
  url_prefix="/blog"
)


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.created_date.desc()).paginate(page, current_app.config.get('POSTS_PER_PAGE', 15), False)
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
