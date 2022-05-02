import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    JWT_SECRET_KEY = 'y&mVNO)ZMe01Wtv'
    JWT_TOKEN_LOCATION = ['cookies']
    #JWT_ACCESS_COOKIE_PATH = '/api/'
    #JWT_REFRESH_COOKIE_PATH = '/api/refresh'
    JWT_COOKIE_CSRF_PROTECT = False
    