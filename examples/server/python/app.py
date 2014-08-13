import datetime
import os
import jwt
from flask import Flask, send_file, request, make_response, g, redirect, \
    url_for, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: refactor and break apart code into modules

# Configuration

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
TOKEN_SECRET = 'keyboard cat'
FACEBOOK_SECRET = '298fb6c080fda239b809ae418bf49700'
GOOGLE_SECRET = 'xGxxgKAObIRUwOKycySkL9Fi'
LINKEDIN_SECRET = '7bDltzdHlP9b42xy'
TWITTER_CONSUMER_KEY = 'vdrg4sqxyTPSRdJHKu4UVVdeD'
TWITTER_CONSUMER_SECRET = 'cUIobhRgRlXsFyObUMg3tBq56EgGSwabmcavQP4fncABvotRMA'
TWITTER_CALLBACK_URL = 'http://localhost:3000'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

client_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'client'))

app = Flask(__name__, static_url_path='', static_folder=client_dir)
app.config.from_object(__name__)

# Database and User Model

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    google = db.Column(db.String(120))
    linkedin = db.Column(db.String(120))
    twitter = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


db.create_all()

# Routes

@app.route('/')
def index():
    return send_file('../../client/index.html')


@app.route('/api/me')
def me():
    users = User.query.all()
    return jsonify(users)


@app.route('/auth/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.check_password(request.json['password']):
        response = jsonify(message='Wrong Email or Password')
        response.status_code = 401
        return response
    payload = dict(
        exp=datetime.datetime.now() + datetime.timedelta(days=7),
        user=dict(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            facebook=user.facebook,
            google=user.google,
            linkedin=user.linkedin,
            twitter=user.twitter
        )
    )
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return jsonify(token=token)


@app.route('/auth/signup', methods=['POST'])
def signup():
    print request.json['email']
    print request.json['password']
    u = User(email=request.json['email'],
             password=request.json['password'])
    db.session.add(u)
    db.session.commit()
    return 'OK'


@app.route('/auth/facebook', methods=['POST'])
def facebook():
    pass


@app.route('/auth/google', methods=['POST'])
def google():
    pass


@app.route('/auth/linkedin', methods=['POST'])
def linkedin():
    pass


@app.route('/auth/twitter')
def twitter():
    pass


if __name__ == '__main__':
    app.run()