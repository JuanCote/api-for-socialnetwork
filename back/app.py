from flask import Flask, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api()

class Main(Resource):
    def get(self):
        return {'girl': 'Andrey'}
    
class Users(Resource):
    def get(self):
        page = int(request.args.get('page'))
        count = int(request.args.get('count'))
        with open('users.json') as f:
            content = json.loads(f.read())
        start_user = (page - 1) * count
        result = {
            'items': []
        }
        for i in range(start_user, page * count):
            result['items'].append(content['items'][i])
        return result
    
api.add_resource(Main, '/api/main')
api.add_resource(Users, '/api/users')
api.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)