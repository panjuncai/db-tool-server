from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    nick_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    role_name = fields.Str()