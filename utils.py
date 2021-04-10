from flask_restx import fields, reqparse
from config import api

class JSendResponse:
    def __init__(self, success, data=None, message=None):
        self.success = success
        self.data = data
        self.message = message

class JsendMarshalFieldConstructor:
    def __init__(self):
        pass
    
    def construct(self, model_name='Resource', data_marshal_field: dict=None):
        return api.model('JSend', {
            'success': fields.Boolean,
            'data': fields.String,
            'message': fields.String
        }) if data_marshal_field is None else api.model(model_name, {
            'success': fields.Boolean,
            'data': fields.Nested(api.model(model_name + '_data', data_marshal_field)),
            'message': fields.String
        })

class RequestParserArgument:
    def __init__(self, _name, _type, _reqeuired):
        self.name = _name
        self.type = _type
        self.required = _reqeuired

class RequestParserConstructor:
    def __init__(self):
        pass

    def construct(self, argument_arr: list):
        rtn = reqparse.RequestParser(bundle_errors=True)
        for argument in argument_arr:
            rtn.add_argument(argument[0], type=argument[1], required=argument[2])
        return rtn

jmfc = JsendMarshalFieldConstructor()
rpc = RequestParserConstructor()