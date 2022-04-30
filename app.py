
from ast import parse
from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import json
from sqlalchemy import Identity, MetaData
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_object(Config)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
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
            start_user = (page - 1) * count
            last_man = page*count
            total_count = models.User.query.count()
            users = models.User.query.all()
            result = {
                'items': [],
                'totalCount': total_count
            }
            for user in users:
                result['items'].append({
                    'name': user.name,
                    'photo': '',
                    'status': user.status
                })
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
                'contacts': {
                    'site': profile.site,
                    'phone_number': profile.phone_number,
                    'email_contact': profile.email_contact,
                    'telegram': profile.telegram,
                    'whatsapp': profile.whatsapp,
                    'discord': profile.discord,
                    'personal': profile.personal
                }
            }
            return jsonify(result)
        return jsonify({'message': 'variables id reqired'})

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        data = parser.parse_args()
        if data['username'] == None or data['email'] == None or data['password'] == None or data['name'] == None or data['surname'] == None:
            return {'resultCode': 1,
                    'message': 'invalid request'}
        if models.User.query.filter_by(username=data['username']).first():
            return {'resultCode': 1,
                    'message': 'username already taken'}
        if models.User.query.filter_by(email=data['email']).first():
            return {'resultCode': 1,
                    'message': 'email already taken'}
        hash = generate_password_hash(data['password'])
        u = models.User(email=data['email'], username=data['username'], password_hash=hash, name=data['name'], surname=data['surname'])
        db.session.add(u)
        db.session.commit()
        return {'resultCode': 0,
                'message': 'new user created'}
    
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
            return {'message': 'user not found'}, 401
        if check_password_hash(user.password_hash, password):
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access)
            set_refresh_cookies(resp, refresh)
            return resp
        else:
            return {'messsage': 'invalid password'}, 401

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access = create_access_token(identity=identity)
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access)
        return resp, 200
        
api.add_resource(Test, '/api/test')
api.add_resource(Users, '/api/users')
api.add_resource(Profile, '/api/profile/<int:id>')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Refresh, '/api/refresh')
api.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    