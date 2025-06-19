from flask import Blueprint, render_template, current_app

routes_bp = Blueprint('routes', __name__)
 
@routes_bp.route('/logs')
def log_monitor():
    """日志监控页面"""
    log_file = current_app.config.get('LOG_MONITOR_FILE', '未配置')
    return render_template('log_monitor.html', log_file=log_file) 