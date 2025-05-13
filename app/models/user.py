from app.models import BaseModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, BaseModel):
    """用户模型类"""
    __tablename__ = 't_user'
    
    # 基本信息
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False, comment='用户名')
    pwd = db.Column(db.String(128), nullable=False, comment='密码')
    nick_name = db.Column(db.String(32), comment='昵称')
    phone = db.Column(db.String(11), unique=True, comment='手机号')
    email = db.Column(db.String(64), unique=True, comment='邮箱')
    avatar = db.Column(db.String(256), comment='头像URL')
    
    # 状态信息
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    is_admin = db.Column(db.Boolean, default=False, comment='是否为管理员')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    
    # 外键关系
    rid = db.Column(db.Integer, db.ForeignKey('t_role.id'), comment='角色ID')
    role = db.relationship('Role', back_populates='users')

    def __init__(self, name, pwd, nick_name=None, phone=None, email=None, rid=None):
        self.name = name
        self.pwd = generate_password_hash(pwd)
        self.nick_name = nick_name or name
        self.phone = phone
        self.email = email
        self.rid = rid

    @property
    def password(self):
        """密码属性，不允许直接访问"""
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        """设置密码，自动进行加密"""
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        """验证密码是否正确"""
        return check_password_hash(self.pwd, password)

    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_private=False):
        """
        将用户对象转换为字典
        Args:
            include_private: 是否包含私密信息
        """
        data = {
            'id': self.id,
            'name': self.name,
            'nick_name': self.nick_name,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'role_name': self.role.name if self.role else None
        }
        
        if include_private:
            data.update({
                'phone': self.phone,
                'email': self.email
            })
            
        return data

    def __repr__(self):
        return f'<User {self.name}>'