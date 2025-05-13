from marshmallow import Schema, fields, EXCLUDE

class BaseSchema(Schema):
    """基础Schema类，包含共用字段"""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        ordered = True  # 保持字段顺序
        unknown = EXCLUDE  # 忽略未知字段

from .user import UserSchema

__all__ = ['UserSchema']


