from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class BaseModel:
    """基础模型类，包含共用字段"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """保存当前记录"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """删除当前记录"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """通过ID获取记录"""
        return cls.query.get(id)

from .user import User
from .role import Role
from .menu import Menu

__all__ = ['User', 'Role', 'Menu']
