import datetime
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request, abort, current_app
from webapp.blog.models import db, Post, Tag
from webapp.auth.models import User
from .fields import HTMLField
from .parsers import post_get_parser

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

