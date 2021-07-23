from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from models import auth_model
from utils import JsendMarshalFieldConstructor, RequestParserConstructor
from utils import jmfc, rpc, JSendResponse

api = Namespace('auth', description='Authentication operation')

@api.route('')
class Auth(Resource):

    # get user id : used for jwt

    @api.doc("Get the user information")
    @api.marshal_with(jmfc.construct('user_id', {
        'id': fields.String
    }))
    @jwt_required()
    def get(self):
        return JSendResponse(True, {"id": current_user['id']})

    # login

    login_parser = rpc.construct([
        ['username', str, True],
        ["password", str, True]
    ])
    @api.doc("Login and get the auth token")
    @api.expect(login_parser, validate=True)
    @api.marshal_with(jmfc.construct('login_package', {
        'auth_token': fields.String
    }))
    def post(self):
        args = Auth.login_parser.parse_args()
        try:
            result = auth_model.get_user_auth(args['username'], args['password'])
            token = create_access_token(identity=result)
            return JSendResponse(True, data={'auth_token': token})
        except Exception as e:
            return JSendResponse(False, message=e)

    # change password

    change_pwd_parser = rpc.construct([
        ['username', str, True],
        ['old_password', str, True],
        ['new_password', str, True],
        ['email', str, True],
        ['code', str, True]
    ])
    @api.doc("Change password")
    @api.expect(change_pwd_parser, validate=True)
    @api.marshal_with(jmfc.construct())
    def put(self):
        try:
            args = Auth.change_pwd_parser.parse_args()
            auth_model.change_password(args["username"], args["old_password"], args["new_password"], args["email"], args["code"])
            return JSendResponse(True)
        except Exception as e:
            return JSendResponse(False, message=e)

@api.route('/registry')
class Registry(Resource):

    # get verification code
    get_code_parser = rpc.construct([
        ['email', str, True]
    ])

    @api.doc("Get verification code")
    @api.expect(get_code_parser, validate=True)
    @api.marshal_with(jmfc.construct())
    def get(self):
        try:
            args = Registry.get_code_parser.parse_args()
            auth_model.get_code(args['email'])
            return JSendResponse(True)
        except Exception as e:
            return JSendResponse(False, message=e)
    
    # register code
    register_parser = rpc.construct([
        ['username', str, True],
        ['password', str, True],
        ['email', str, True],
        ['code', str, True]
    ])
    @api.expect(register_parser, validate=True)
    @api.marshal_with(jmfc.construct())
    def put(self):
        try:
            args = Registry.register_parser.parse_args()
            auth_model.register(args['username'], args['password'], args['email'], args['code'])
            return JSendResponse(True)
        except Exception as e:
            return JSendResponse(False, message=e)