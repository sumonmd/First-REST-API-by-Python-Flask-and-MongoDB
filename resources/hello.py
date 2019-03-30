from flask_restful import Resource

class Hello(Resource):
    def add(self):
        return {"message": "Welcome to Python Coding"}
