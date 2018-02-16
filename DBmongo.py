import pymongo
from flask import Flask,request
from flask_restful import Resource ,Api ,reqparse
from datetime import datetime,date

client = pymongo.MongoClient('localhost',27017)

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('emp_number')

db = client.admin.system_network

class regis(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['emp_number']
                firstname = args['firstname']
                lastname = args['lastname']
                password = args['password']
                data = db.find_one({"user.emp_number":id})
                if(data):
                        return {"wrong!":"has exits this ID"}
                db.insert({"user":{"emp_number":id,"firstname":firstname,
				"lastname":lastname,"password":password},"list":[]})
                return {"firstname":firstname,"lastname":lastname,
				"emp_number":id,"password":password}

class login(Resource):
        def post(self):
                args = parser.parse_args()
                username = args['username']
                password = args['password']
                data = db.find_one({"user.emp_number":username,"user.password":password})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        datetime_login = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        db.update({"user.emp_number":username},{"$push":{"list":{"datetime":datetime_login}}})
                        return {"firstname":firstname,"lastname":lastname,"datetime":datetime_login}
                return {}

class history(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['id']
                data = db.find_one({"user.emp_number":id})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        list_work = data['list']
                        return {"firstname":firstname,"lastname":lastname,"list":list_work}
                return {}
api.add_resource(regis,'/api/reg')
api.add_resource(login,'/api/login')
api.add_resource(history,'/api/history')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5500)
