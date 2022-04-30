
from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Api, Resource
from flask_cors import CORS
import json
<<<<<<< HEAD
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
=======
from sqlalchemy import Identity, MetaData
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)
>>>>>>> 1c5e320b2c3c7a8ec0cb074148f4b4ee0ebbab9c

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api()
CORS(app)

import models

class Test(Resource):
    @jwt_required()
    def get(self):
        return {'girl': 'Andrey'}
    
class Users(Resource):
    @jwt_required()
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
    
<<<<<<< HEAD
api.add_resource(Test, '/api/test')
api.add_resource(Users, '/api/users')
api.add_resource(Profile, '/api/profile/<int:id>')
=======
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        data = parser.parse_args()
        if data['username'] == None or data['password'] == None:
            return {'message': 'invalid request'}
        password = data['password']
        if '@' in data['username']:
            user = models.User.query.filter_by(email=data['username']).first()
        else:
            user = models.User.query.filter_by(username=data['username']).first()
        if user == None:
            return {'message': 'user not found'}
        if check_password_hash(user.password_hash, password):
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)
            return {
                'access': access,
                'refresh': refresh
            }

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access = create_access_token(identity=identity)
        return {
            'access': access
        }
        
api.add_resource(Test, '/api/test')
api.add_resource(Users, '/api/users')
api.add_resource(Profile, '/api/profile/<int:id>')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Refresh, '/api/refresh')
>>>>>>> 1c5e320b2c3c7a8ec0cb074148f4b4ee0ebbab9c
api.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)