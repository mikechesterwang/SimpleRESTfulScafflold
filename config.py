from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
import datetime
import pymysql

app = Flask(__name__)
app = Flask(__name__, static_folder="static", static_url_path="")

ip = 'localhost'
port = 6888
app.config["JWT_SECRET_KEY"] = "a5c686e5170e135b4aa99eef81849451c75ebea2ced62ebd33576862bac0d7da8322db476b42e2ffa6b426fa800a48dfca4c0e07416adbb2edb237ae3a5393c2"
app.config['PROPAGATE_EXCEPTIONS'] = True # https://github.com/vimalloc/flask-jwt-extended/issues/246
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=2)
api = Api(app, version='1.0', title='Sample', description='Simple RESTful scaffold')
jwt = JWTManager(app)

def connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="sedb",
        cursorclass=pymysql.cursors.DictCursor
    )