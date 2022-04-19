
from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
import json
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api()
CORS(app)

import models

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
class Profile(Resource):
    def get(self, id):
        if id:
            profile = models.User.query.filter_by(id=id).first()
            if profile is None:
                return jsonify({'message': 'invalid id'})
            result = {
                'id': 1,
                'name': profile.name,
                'surname': profile.surname,
                'status': profile.status,
                'description': profile.description,
                'job_status': profile.job_status,
                'job_descritpion': profile.job_description,
                'site': profile.site,
                'phone_number': profile.phone_number,
                'email_contact': profile.email_contact,
                'telegram': profile.telegram,
                'whatsapp': profile.whatsapp,
                'discord': profile.discord,
                'personal': profile.personal
            }
            return jsonify(result)
        return jsonify({'message': 'variables id reqired'})
    
api.add_resource(Test, '/api/test')
api.add_resource(Users, '/api/users')
api.add_resource(Profile, '/api/profile/<int:id>')
api.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)