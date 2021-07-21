# Simple RESTful scaffold

A simple Flask RESTful + Swagger + JWT Authorization + MySQL solution.



### Set up

1. Install all requirements in `requirements.txt`

2. rename `config-sample.py` to `config.py` and modify the following variables:

   ​	`ip`: ip address of your application

   ​	`port`: port of your application

   ​	`app.config["JWT_SECRET_KEY"]`: Secret key for JWT authorization

   ​	`connection`: The MySQL connector

3. Create a `user` table in database. The table should contains the following fields:
   1. `id`: INT, primary key, auto Increment
   2. `username`: varchar(512), not null
   3. `password`: varchar(512), not null
   4. `email`: varchar(512), not null
   5. `status`: varchar(45), null (This field is unused.)

4. Create a `verification_code` table in database. The table should contains the following fields:
   1. `email`: VARCHAR(512), primary key, not null
   2. `code`: VARCHAR(8), not null
   3. `created_time`: DATETIME, not null

5. Run `python server.py`



### Documentations

1. JWT authorization: https://flask-jwt-extended.readthedocs.io/en/stable/
2. Restx (RESTful + swagger): https://flask-restx.readthedocs.io/en/latest/
3. PyMySQL: https://pymysql.readthedocs.io/en/latest/



### Authorization

```
POST /auth
```

Post payload

```json
{
	"username": "admin",
    "password": "admin"
}
```

Response example

```json
{
    "success": true,
    "data": {
        "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ1.eyJmcmVzaCI6ZmFsc3UsImlhdCI6MTYxODAzNDMwMywianRpIjoiMTBlMWY4YjktYTdhNC00YjM0LWI3YmQtYTUyYzczYTMwODYyIiwibmJmIjoxNjE4MDM0MzAzLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTgwMzUyMDN9.2GVphwZgA8fQ7fS4DdP-iroCgqIuWPEXtBOL00M5S3M"
    },
    "message": null
}
```

Then send request to JWT protected API with the `auth_token`. Type of the authorization is `Bearer Token`.



### Workflow

create a API namespace in `apis/`, for example, `test.py`

```python
api = Namespace('test', description='Test operation')

# Route
@api.route('')
class Test(Resource):
    # For swagger UI generation
    @api.doc("Get the user information")
    # Claim the data field structure of the response.
    # For swagger UI generation and marshalling.
    @api.marshal_with(jmfc.construct('user_id', { 
        'id': fields.String
    }))
    # JWT authorization protection
    @jwt_required()
    def get(self):
        return JSendResponse(True, {"id": current_user['id']})
```

create a model file in `models/`, then use it for database operation.

register the API namespace in `server.py`

```python
from apis.test import api as test_ns
api.add_namespace(test_ns)
```



