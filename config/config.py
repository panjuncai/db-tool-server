import os

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_please_change_in_production'
    
    # 数据库配置
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'flask_shop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_dev_key_please_change_in_production'
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24 小时

    # 允许的图片类型
    ALLOWED_IMGS = {'bmp', 'png', 'jpg', 'jpeg', 'gif'}
    
    # 图片上传路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    IMG_UPLOAD_DIR = os.path.join(STATIC_DIR, 'img')
    
    # 确保必要的目录存在
    @staticmethod
    def init_app(app):
        os.makedirs(Config.STATIC_DIR, exist_ok=True)
        os.makedirs(Config.IMG_UPLOAD_DIR, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}