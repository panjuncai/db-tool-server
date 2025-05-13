from app.models import User
from app import db
from app.utils import to_dict_msg, generate_auth_token
from werkzeug.security import generate_password_hash, check_password_hash
import re


class UserService:
    def create_user(self, username, password, email=None, phone=None, rid=None):
        """
        创建新用户
        """
        try:
            # 检查用户名是否已存在
            if User.query.filter_by(name=username).first():
                raise ValueError("用户名已存在")

            # 创建新用户
            user = User(
                name=username,
                pwd=password,  # __init__中会自动进行密码加密
                email=email,
                phone=phone,
                rid=rid
            )
            
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            
            return self._to_dict(user)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"创建用户失败: {str(e)}")

    def get_user_by_id(self, user_id):
        """
        通过ID获取用户信息
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError("用户不存在")
        return self._to_dict(user)

    def update_user(self, user_id, username=None, password=None, email=None, phone=None):
        """
        更新用户信息
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("用户不存在")

            # 如果要更改用户名，检查新用户名是否已存在
            if username and username != user.name:
                if User.query.filter_by(name=username).first():
                    raise ValueError("新用户名已存在")
                user.name = username

            # 更新其他字段
            if password:
                user.pwd = generate_password_hash(password)
            if email:
                self._validate_email(email)
                user.email = email
            if phone:
                self._validate_phone(phone)
                user.phone = phone

            db.session.commit()
            return self._to_dict(user)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"更新用户信息失败: {str(e)}")

    def delete_user(self, user_id):
        """
        删除用户
        """
        try:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("用户不存在")
            
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"删除用户失败: {str(e)}")

    def login(self, username, password):
        """
        用户登录
        """
        user = User.query.filter_by(name=username).first()
        if not user:
            raise ValueError("用户名或密码错误")

        if not check_password_hash(user.pwd, password):
            raise ValueError("用户名或密码错误")

        # 生成认证令牌
        token = generate_auth_token(user.id)
        return token

    def _validate_email(self, email):
        """
        验证邮箱格式
        """
        if email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                raise ValueError("邮箱格式不正确")

    def _validate_phone(self, phone):
        """
        验证手机号格式
        """
        if phone:
            pattern = r'^1[3-9]\d{9}$'
            if not re.match(pattern, phone):
                raise ValueError("手机号格式不正确")

    def _to_dict(self, user):
        """
        将用户对象转换为字典
        """
        return {
            'id': user.id,
            'username': user.name,  # 转换为前端期望的字段名
            'email': user.email,
            'phone': user.phone,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else None
        }