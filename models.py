from enum import unique
from sqlalchemy import ForeignKey
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    avatar = db.Column(db.BLOB)
    status = db.Column(db.Text(500))
    description = db.Column(db.Text(500))
    job_status = db.Column(db.Boolean)
    job_description = db.Column(db.String)
    site = db.Column(db.String)
    phone_number = db.Column(db.String)
    email_contact = db.Column(db.String)
    telegram = db.Column(db.String)
    whatsapp = db.Column(db.String)
    discord = db.Column(db.String)
    personal = db.Column(db.String)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    