from flask_restplus import Model, fields

auth_dto = Model('auth_details', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password '),
})
