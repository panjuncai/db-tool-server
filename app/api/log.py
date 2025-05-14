from flask import Blueprint, jsonify, request, current_app, Response, stream_with_context
from app.utils import LogMonitor
import time
import json

log_bp = Blueprint('log', __name__, url_prefix='/api/log')

@log_bp.route('/', methods=['GET'])
def get_log():
    """获取日志文件内容"""
    max_lines = request.args.get('max_lines', type=int)
    log_data = LogMonitor.get_log_content(max_lines)
    return jsonify({
        'code': 200,
        'message': '获取日志内容成功',
        'data': log_data
    })

@log_bp.route('/stream', methods=['GET'])
def stream_log():
    """流式获取日志内容（Server-Sent Events）"""
    max_lines = request.args.get('max_lines', type=int)
    interval = request.args.get('interval', 
                               type=int, 
                               default=current_app.config.get('LOG_MONITOR_UPDATE_INTERVAL', 5))
    
    def generate():
        try:
            for log_data in LogMonitor.tail_log(max_lines=max_lines, follow=True, interval=interval):
                # 使用SSE格式
                yield f"data: {json.dumps(log_data)}\n\n"
        except GeneratorExit:
            # 客户端断开连接
            pass
    
    return Response(stream_with_context(generate()),
                   mimetype="text/event-stream",
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'X-Accel-Buffering': 'no'  # 禁用Nginx缓冲
                   })

@log_bp.route('/info', methods=['GET'])
def get_log_info():
    """获取日志文件信息"""
    log_file = current_app.config.get('LOG_MONITOR_FILE')
    try:
        import os
        from datetime import datetime
        
        if not log_file or not os.path.exists(log_file):
            return jsonify({
                'code': 404,
                'message': f'日志文件不存在',
                'data': {
                    'file_path': log_file,
                    'exists': False
                }
            }), 404
            
        # 获取文件信息
        file_stats = os.stat(log_file)
        
        return jsonify({
            'code': 200,
            'message': '获取日志文件信息成功',
            'data': {
                'file_path': log_file,
                'file_size': file_stats.st_size,
                'last_modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'exists': True
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取日志信息失败: {str(e)}',
            'data': {
                'file_path': log_file
            }
        }), 500 