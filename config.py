from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
import pymysql

app = Flask(__name__)

ip = 'localhost'
port = 6888
app.config["JWT_SECRET_KEY"] = "a5c686e5170e135b4aa99eef81849451c75ebea2ced62ebd33576862bac0d7da8322db476b42e2ffa6b426fa800a48dfca4c0e07416adbb2edb237ae3a5393c2"

app.config['PROPAGATE_EXCEPTIONS'] = True # https://github.com/vimalloc/flask-jwt-extended/issues/246
api = Api(app, version='1.0', title='Sample', description='Simple RESTful scaffold')
jwt = JWTManager(app)

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="sedb",
    cursorclass=pymysql.cursors.DictCursor
)

# https://flask-jwt-extended.readthedocs.io/en/stable/api/#module-flask_jwt_extended

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['id']

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    with connection.cursor() as cursor:
        sql = "SELECT `id` FROM `user` WHERE `id`=%s"
        cursor.execute(sql, (identity))
        return cursor.fetchone()