import time
import threading
from flask import current_app
from app.utils import LogMonitor
from flask_socketio import emit, disconnect
import socketio

class LogNamespace:
    """日志监控WebSocket命名空间"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.threads = {}
        self.stop_events = {}
        self.app = None
        
        # 保存应用实例引用（稍后在线程中使用）
        if current_app:
            self.app = current_app._get_current_object()
        
        # 注册事件处理函数
        @socketio.on('connect', namespace='/logs')
        def handle_connect():
            print('客户端连接 - 日志监控')
        
        @socketio.on('disconnect', namespace='/logs')
        def handle_disconnect():
            print('客户端断开连接 - 日志监控')
            # 停止该客户端的监控线程
            client_id = get_client_id()
            self.stop_log_monitor(client_id)
        
        @socketio.on('start_log_monitor', namespace='/logs')
        def handle_start_monitor(data):
            client_id = get_client_id()
            max_lines = data.get('max_lines')
            interval = data.get('interval')
            self.start_log_monitor(client_id, max_lines, interval)
            return {'status': 'success', 'message': '开始监控日志'}
        
        @socketio.on('stop_log_monitor', namespace='/logs')
        def handle_stop_monitor():
            client_id = get_client_id()
            self.stop_log_monitor(client_id)
            return {'status': 'success', 'message': '停止监控日志'}
        
        @socketio.on('get_log', namespace='/logs')
        def handle_get_log(data):
            max_lines = data.get('max_lines')
            log_data = LogMonitor.get_log_content(max_lines)
            return log_data
    
    def start_log_monitor(self, client_id, max_lines=None, interval=None):
        """启动日志监控线程"""
        # 如果已有监控线程，先停止
        self.stop_log_monitor(client_id)
        
        # 创建停止事件
        stop_event = threading.Event()
        self.stop_events[client_id] = stop_event
        
        # 创建并启动监控线程
        log_thread = threading.Thread(
            target=self._log_monitor_worker,
            args=(client_id, stop_event, max_lines, interval)
        )
        log_thread.daemon = True
        log_thread.start()
        
        self.threads[client_id] = log_thread
    
    def stop_log_monitor(self, client_id):
        """停止日志监控线程"""
        if client_id in self.stop_events:
            self.stop_events[client_id].set()
            if client_id in self.threads:
                # 等待线程结束，但不阻塞太久
                self.threads[client_id].join(timeout=0.5)
                del self.threads[client_id]
            del self.stop_events[client_id]
    
    def _log_monitor_worker(self, client_id, stop_event, max_lines=None, interval=None):
        """日志监控线程工作函数"""
        if not self.app:
            print("警告: 没有有效的应用实例，无法监控日志")
            return
            
        # 使用应用上下文
        with self.app.app_context():
            if interval is None:
                interval = current_app.config.get('LOG_MONITOR_UPDATE_INTERVAL', 5)
            
            log_file = current_app.config.get('LOG_MONITOR_FILE')
            print(f"开始监控日志文件: {log_file}")
            
            # 先发送一次日志数据
            try:
                log_data = LogMonitor.get_log_content(max_lines)
                self.socketio.emit('log_update', log_data, namespace='/logs', to=client_id)
                
                while not stop_event.is_set():
                    # 检查日志文件是否有变化
                    new_log_data = LogMonitor.get_log_content(max_lines)
                    if new_log_data['file_size'] != log_data['file_size']:
                        self.socketio.emit('log_update', new_log_data, namespace='/logs', to=client_id)
                        log_data = new_log_data
                    
                    # 等待一段时间
                    stop_event.wait(interval)
            except Exception as e:
                print(f"日志监控错误: {str(e)}")
                self.socketio.emit('log_error', {'error': str(e)}, namespace='/logs', to=client_id)

def get_client_id():
    """获取当前客户端的ID"""
    # 在Flask-SocketIO的新版本中，应该使用socketio.rooms方法获取session ID
    try:
        # 不同版本的Flask-SocketIO获取sid的方式不同
        from flask import request
        if hasattr(request, 'sid'):
            return request.sid
            
        from flask_socketio import rooms
        return rooms()[0]
    except Exception as e:
        print(f"获取客户端ID失败: {str(e)}")
        # 如果无法获取到ID，返回一个随机ID避免程序崩溃
        import uuid
        return str(uuid.uuid4())

def init_socketio(socketio):
    """初始化SocketIO"""
    LogNamespace(socketio) 