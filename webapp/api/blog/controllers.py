from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

class PostApi(Resource):
    @jwt_required
    def get(self):
        return jsonify("Hello World")

