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

verification_code_email = {
    "smtp": {
        "email": "xxxx@xxx.com",
        "password": "123456",
        "host": "smtp.163.com",
        "port": 465
    },

    "email": {
        "subject": "[TeamX] verification code",
        "content-type": "html", #utf8
        "content": """\
            <html>
            <head></head>
            <body>
                <div style="width: 320px; height: 200px; border-radius: 34px;
            background: linear-gradient(145deg, #ffffff, #e1e1e1);
            box-shadow:  16px 16px 39px #d5d5d5,
                        -16px -16px 39px #ffffff; display: flex; flex-direction: column; justify-content: center; align-items:center;">
                    <p>Your verification code is</p>
                    <h2>{}</h2>
                </div>
                <br />
                <br />
                <p>TeamX</p>
            </body>
            </html>
            """
    }
}

def connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        database="sedb",
        cursorclass=pymysql.cursors.DictCursor
    )