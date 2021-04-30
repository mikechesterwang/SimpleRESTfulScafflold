from config import api, app, jwt, ip, port, connection
from apis.auth import api as auth_ns
from flask import send_from_directory

api.add_namespace(auth_ns)

# https://flask-jwt-extended.readthedocs.io/en/stable/api/#module-flask_jwt_extended

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['id']

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    with connection().cursor() as cursor:
        sql = "SELECT `id` FROM `user` WHERE `id`=%s"
        cursor.execute(sql, (identity))
        return cursor.fetchone()

if __name__ == "__main__":
    app.run(ip, port)