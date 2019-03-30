from flask import Flask, jsonify, request
from flask_restful import Resource
import ast
import pymongo

connection = pymongo.MongoClient('localhost', 27017)
database = connection['myDatabase']
data_collection = database['mycollection']


class Page(Resource):

    def get(self):
        feed11 = 0
        feed_count11 = 0
        last_feed11_id = 0
        feed12 = 0
        feed_count12 = 0
        last_feed11_id = 0
        feed16 = 0
        feed_count16 = 0
        last_feed11_id = 0
        output = []
        limits = 48
        list11 = ""
        list12 = ""
        list16 = ""
        remain11 = 0
        remain12 = 0
        remain16 = 0
        need_feed11_ratio = 0
        need_feed12_ratio = 0
        need_feed16_ratio = 0
        last_pos11 = 0
        last_pos12 = 0
        last_pos16 = 0
        feed11_ratio = 0
        feed12_ratio = 0
        feed16_ratio = 0
        limits = 48


#------when feed_ratio not in url but page in url----------
        if ('feed_ratio' not in request.args and 'page' in request.args):
            try:
             pgs =int(request.args['page'])
            except ValueError:
                return "Please Press valid page Number such as 1,2,3....",400

            if pgs >= 0 and pgs < 5:
                page = pgs
                pgs = pgs * limits
                start_id = data_collection.find().sort('id', pymongo.ASCENDING)
                last_id = start_id[pgs]['id']
                datas = data_collection.find({'id': {'$gte': last_id}}).sort('id', pymongo.ASCENDING).limit(limits)

                for i in datas:
                    output.append(
                        {'id': i['id'], 'feed': i['feed'], 'property_name': i['property_name'], 'price': i['price']})
                return jsonify({"Starting Page Number":0,"Current Page Number":page,"Total Data":200},{'Paginations': output},200)
            else:
                return  "Invalid url! Please press in Page number = 0 to 4",400

#-----------when feed_ratio and page not in url--------------

        elif('feed_ratio' not in request.args and 'page' not in request.args):
            data_list = []

            data = data_collection.find({})
            for i in data:
                data_list.append(str(i))
            return {"Total Data":200,"Single Page":"All Data Here","data": data_list}, 200

    #-------When feed_ratio and page in url-------------------

        elif('feed_ratio' in request.args and 'page' in request.args):
            try:
                ofset = request.args['feed_ratio']
                offset = ast.literal_eval(ofset)
                pgs = int(request.args['page'])
            except ValueError:
                return "Please Valid Url such as http://localhost:5000/api/properties?feed_ratio=[{'feed':11,'ratio':25},{'feed':12,'ratio':25},{'feed':16,'ratio':25}]&page=1",400

            for x in offset:
                if (x['feed'] == 11):
                    feed11 = x['ratio']
                if (x['feed'] == 12):
                    feed12 = x['ratio']
                if (x['feed'] == 16):
                    feed16 = x['ratio']


            if ((feed11 + feed12 + feed16) != 48 or pgs>=4):
                return "404 page Invalid Url :Cross or down limited feed_ratio | please type http://localhost:5000/api/properties?feed_ratio=[{'feed':11,'ratio':16},{'feed':12,'ratio':16},{'feed':16,'ratio':16}]&page=0",400
            else:
                feed_ratio = data_collection.find().sort('id', pymongo.ASCENDING)
                for x in feed_ratio:
                    if (x['feed'] == 11):
                        feed_count11 += 1
                    if (x['feed'] == 12):
                        feed_count12 += 1
                    if (x['feed']) == 16:
                        feed_count16 += 1
                last_feed11_id = pgs * feed11
                last_feed12_id = pgs * feed12
                last_feed16_id = pgs * feed16

                list11 = data_collection.find({'feed': 11}).sort('id', pymongo.ASCENDING) # store feed_11 type
                list12 = data_collection.find({'feed': 12}).sort('id', pymongo.ASCENDING) #store feed_12 type
                list16 = data_collection.find({'feed': 16}).sort('id', pymongo.ASCENDING) #store feed_16 type

                if (list11.count() > last_feed11_id):
                    last_pos11 = list11[last_feed11_id]['id']
                if (list12.count() > last_feed12_id):
                    last_pos12 = list12[last_feed12_id]['id']
                if (list16.count() > last_feed16_id):
                    last_pos16 = list16[last_feed16_id]['id']


                if (list11.count() >= last_feed11_id):
                    remain_list11 = list11.count() - last_feed11_id
                    if (remain_list11 >= feed11):
                        feed11_ratio = data_collection.find({'feed': 11, 'id': {'$gte': last_pos11}}).sort('id',pymongo.ASCENDING).limit( feed11)


                    elif remain_list11 < feed11 and remain_list11 > 0:
                        feed11_ratio = data_collection.find({'feed': 11, 'id': {'$gte': last_pos11}}).sort('id',pymongo.ASCENDING).limit(remain_list11)
                        need_feed11_ratio = feed11 - remain_list11

                    else:
                        feed11_ratio = ""
                else:
                    feed11_ratio =None
                # for feed12-----------
                if (list12.count() >= last_feed12_id):
                    remain_list12 = list12.count() - last_feed12_id
                    if (remain_list12 >= feed12):
                        if (need_feed11_ratio and (remain_list12 > need_feed11_ratio)):
                            data_collection.find({'feed': 12, 'id': {'$gte': last_pos12}}).sort('id', pymongo.ASCENDING).limit(feed12 + need_feed12_ratio)
                        else:
                            feed12_ratio = data_collection.find({'feed': 12, 'id': {'$gte': last_pos12}}).sort('id',pymongo.ASCENDING).limit(feed12)

                    elif remain_list12 < feed12 and remain_list12 > 0:
                        feed12_ratio = data_collection.find({'feed': 12, 'id': {'$gte': last_pos12}}).sort('id',pymongo.ASCENDING).limit(remain_list12)


                        need_feed12_ratio = feed12 - remain_list12
                else:
                    feed12_ratio = 0

                # for feed16-----------
                if (list16.count() >= last_feed16_id):
                    remain_list16 = list12.count() - last_feed16_id
                    if (remain_list16 >= feed16):
                        if (need_feed11_ratio and (remain_list16 > need_feed11_ratio)):
                            feed16_ratio = data_collection.find({'feed': 16, 'id': {'$gte': last_pos16}}).sort('id',pymongo.ASCENDING).limit(feed16 + need_feed11_ratio)


                        elif (need_feed12_ratio and (remain_list16 > need_feed12_ratio)):
                            feed16_ratio = data_collection.find({'feed': 16, 'id': {'$gte': last_pos16}}).sort('id',pymongo.ASCENDING).limit(feed16 + need_feed12_ratio)


                        else:
                            feed16_ratio = data_collection.find({'feed': 16, 'id': {'$gte': last_pos16}}).sort('id',pymongo.ASCENDING).limit(feed16)


                    elif remain_list16 < feed16 and remain_list16 > 0:
                        feed16_ratio = data_collection.find({'feed': 16, 'id': {'$gte': last_pos16}}).sort('id',pymongo.ASCENDING).limit(remain_list16)


                        need_feed16_ratio = feed11 - remain_list16


                else:
                    feed16_ratio = None

                if (feed11_ratio):
                    for i in feed11_ratio:
                        output.append(str(i))
                if (feed12_ratio):
                    for j in feed12_ratio:
                        output.append(str(j))
                if (feed16_ratio):
                    for k in feed16_ratio:
                        output.append(str(k))

                return jsonify({"Current Page Number":pgs,"Starting page":" 0","Total Data ": 200,},{"output":output},200)














