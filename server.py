from config import api, app, ip, port
from apis.auth import api as auth_ns

api.add_namespace(auth_ns)

if __name__ == "__main__":
    app.run(ip, port)