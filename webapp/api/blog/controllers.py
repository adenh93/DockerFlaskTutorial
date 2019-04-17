import datetime
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request, abort, current_app
from webapp.blog.models import db, Post, Tag
from webapp.auth.models import User
from .fields import HTMLField
from .parsers import post_get_parser, post_post_parser, post_put_parser

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'id': fields.Integer(),
    'title': fields.String(),
    'body': HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'created_date': fields.DateTime(dt_format='iso8601')
}

def add_tags_to_post(post, tags_list):
    for item in tags_list:
        tag = Tag.query.filter_by(title=item).first()

        if tag:
            post.tags.append(tag)
        else:
            new_tag = Tag(item)
            post.tags.append(new_tag)


class PostApi(Resource):
    @marshal_with(post_fields)
    @jwt_required
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            return post
        else:
            args = post_get_parser.parse_args() 
            page = args['page'] or 1 
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)
                posts = user.posts.order_by(
                    Post.created_date.desc()
                ).paginate(page, current_app.config.get('POSTS_PER_PAGE', 10))
            else:
                posts = Post.query.order_by( 
                    Post.created_date.desc() 
                ).paginate(page, current_app.config.get('POSTS_PER_PAGE', 10))
            return posts.items
    
    @jwt_required
    def post(self, post_id=None):  
        args = post_post_parser.parse_args(strict=True) 
        new_post = Post(args['title'])
        new_post.user_id = get_jwt_identity()
        new_post.body = args['body'] 
        if args['tags']:
            add_tags_to_post(new_post, args['tags']) 
        db.session.add(new_post) 
        db.session.commit()
        return {'id': new_post.id}, 201

    @jwt_required
    def put(self, post_id=None):
        if not post_id:
            abort(400)
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        args = post_put_parser.parse_args(strict=True)
        if get_jwt_identity() != post.user_id:
            abort(403)
        if args['title']:
            post.title = args['title']
        if args['body']:
            post.body = args['body']
        if args['tags']:
            add_tags_to_post(post, args['tags'])
        db.session.merge(post)
        db.session.commit()
        return {'id': post.id}, 201

