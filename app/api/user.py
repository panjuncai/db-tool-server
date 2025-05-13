from flask import Blueprint, g
from flask_restful import Api, Resource, reqparse
from app.services import UserService
from app.utils import to_dict_msg, login_required

user_bp = Blueprint('user', __name__, url_prefix='/api')
user_api = Api(user_bp)

class UserResource(Resource):
    def __init__(self):
        self.user_service = UserService()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, 
                                 help='用户名不能为空')
        self.reqparse.add_argument('pwd', type=str, required=True, 
                                 help='密码不能为空')
        self.reqparse.add_argument('email', type=str)
        self.reqparse.add_argument('phone', type=str)
        self.reqparse.add_argument('rid', type=int)

    @login_required
    def get(self):
        """获取当前用户信息"""
        try:
            user = self.user_service.get_user_by_id(g.user_id)
            return to_dict_msg(status=200, data=user, msg="获取用户信息成功")
        except Exception as e:
            return to_dict_msg(status=500, msg=str(e))

    def post(self):
        """创建新用户"""
        args = self.reqparse.parse_args()
        try:
            user = self.user_service.create_user(
                username=args.name,
                password=args.pwd,
                email=args.email,
                phone=args.phone,
                rid=args.rid
            )
            return to_dict_msg(status=200, data=user, msg="用户创建成功")
        except Exception as e:
            return to_dict_msg(status=500, msg=str(e))

    @login_required
    def put(self):
        """更新用户信息"""
        args = self.reqparse.parse_args()
        try:
            user = self.user_service.update_user(
                user_id=g.user_id,
                name=args.name,
                pwd=args.pwd,
                email=args.email,
                phone=args.phone
            )
            return to_dict_msg(status=200, data=user, msg="用户信息更新成功")
        except Exception as e:
            return to_dict_msg(status=500, msg=str(e))

    @login_required
    def delete(self):
        """删除用户"""
        try:
            self.user_service.delete_user(g.user_id)
            return to_dict_msg(status=200, msg="用户删除成功")
        except Exception as e:
            return to_dict_msg(status=500, msg=str(e))

# 用户登录接口
class UserLoginResource(Resource):
    def __init__(self):
        self.user_service = UserService()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, 
                                 help='用户名不能为空')
        self.reqparse.add_argument('pwd', type=str, required=True, 
                                 help='密码不能为空')

    def post(self):
        """用户登录"""
        args = self.reqparse.parse_args()
        try:
            token = self.user_service.login(
                name=args.name,
                pwd=args.pwd
            )
            return to_dict_msg(status=200, data={'token': token}, msg="登录成功")
        except Exception as e:
            return to_dict_msg(status=401, msg=str(e))

user_api.add_resource(UserResource, '/user')
user_api.add_resource(UserLoginResource, '/login')

@user_bp.errorhandler(Exception)
def handle_error(error):
    return to_dict_msg(status=500, msg=str(error))