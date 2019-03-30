from flask import Flask,jsonify, request
from flask_restful import Resource
import random
import pymongo
from faker import Faker
connection = pymongo.MongoClient('localhost',27017)
database   = connection['myDatabase']
data_collection = database['mycollection']



class Category(Resource):
    def get(self):
        data_list=[]

        data=data_collection.find({})
        for i in data:
            data_list.append(str(i))
        return {"data":data_list},200

    def post(self):
        fed=[11,12,16]
        fake=Faker()
        for i in range(1,200):
            value={
                'id':i,
                'feed':random.choice(fed),
                'property_name':fake.name(),
                'price' :random.randint(100,400)
            }
            data_collection.insert(value)



