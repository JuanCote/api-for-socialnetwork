
from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
import json

app = Flask(__name__)
api = Api()
CORS(app)

class Test(Resource):
    def get(self):
        return {'girl': 'Andrey'}
    
class Users(Resource):
    def get(self):
        page = request.args.get('page')
        count = request.args.get('count')
        if page and count:
            count = int(count)
            page = int(page)
            with open('users.json') as f:
                content = json.loads(f.read())
            start_user = (page - 1) * count
            result = {
                'items': []
            }
            last_man = page*count
            if last_man > int(content['totalCount']):
                last_man = content['totalCount']
            for i in range(start_user, int(last_man)):
                result['items'].append(content['items'][i])
            result["totalCount"] = content['totalCount']
            result['error'] = content['error']
            return jsonify(result)
        return jsonify({'message': 'variables count and page required'})
    
api.add_resource(Test, '/api/test')
api.add_resource(Users, '/api/users')
api.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)