import jwt
from datetime import datetime, timedelta
from flask import current_app

# 默认的密钥和过期时间
DEFAULT_SECRET_KEY = 'your-secret-key-please-change-in-production'
DEFAULT_EXPIRATION = 24  # 小时

def generate_auth_token(user_id, expiration=DEFAULT_EXPIRATION):
    """
    生成认证令牌
    
    Args:
        user_id: 用户ID
        expiration: 过期时间（小时），默认24小时
        
    Returns:
        str: JWT令牌
    """
    try:
        # 获取配置的密钥，如果没有则使用默认密钥
        secret_key = current_app.config.get('SECRET_KEY', DEFAULT_SECRET_KEY)
        
        # 设置payload
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiration),
            'iat': datetime.utcnow()
        }
        
        # 生成令牌
        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
        
        return token
    except Exception as e:
        raise Exception(f"Token generation failed: {str(e)}")

def verify_auth_token(token):
    """
    验证认证令牌
    
    Args:
        token: JWT令牌
        
    Returns:
        int: 用户ID
        
    Raises:
        Exception: 令牌无效或已过期
    """
    try:
        # 获取配置的密钥，如果没有则使用默认密钥
        secret_key = current_app.config.get('SECRET_KEY', DEFAULT_SECRET_KEY)
        
        # 解码并验证令牌
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=['HS256']
        )
        
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")

def get_token_expiration(token):
    """
    获取令牌的过期时间
    
    Args:
        token: JWT令牌
        
    Returns:
        datetime: 过期时间
    """
    try:
        secret_key = current_app.config.get('SECRET_KEY', DEFAULT_SECRET_KEY)
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return datetime.fromtimestamp(payload['exp'])
    except Exception:
        return None 