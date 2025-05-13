from functools import wraps
from flask import request, g
from app.utils.tokens import verify_auth_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'status': 401, 'msg': '未登录'}
        try:
            user_id = verify_auth_token(token)
            g.user_id = user_id
            return f(*args, **kwargs)
        except:
            return {'status': 401, 'msg': '登录已过期'}
    return decorated_function