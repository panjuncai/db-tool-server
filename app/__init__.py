from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config.config import config

# 创建扩展对象
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    创建Flask应用
    :param config_name: 配置名称，默认为default
    :return: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # 注册蓝图
    from app.api import user_bp, dept_bp, emp_bp, bonus_bp, salgrade_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(dept_bp)
    app.register_blueprint(emp_bp)
    app.register_blueprint(bonus_bp)
    app.register_blueprint(salgrade_bp)
    
    return app