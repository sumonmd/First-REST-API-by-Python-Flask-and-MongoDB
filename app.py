from flask import Blueprint
from flask_restful import Api
from resources.hello import Hello
from resources.category import Category
from resources.page import Page


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/')
api.add_resource(Category,'/categories')
api.add_resource(Page,'/properties')
