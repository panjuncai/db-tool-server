import os
import time
from datetime import datetime
from flask import current_app

class LogMonitor:
    """日志监控类，用于读取和监控日志文件"""
    
    @staticmethod
    def get_log_content(max_lines=None):
        """
        获取日志文件内容
        
        Args:
            max_lines: 最大返回行数，默认使用配置中的值
            
        Returns:
            dict: 包含日志内容、文件信息的字典
        """
        if max_lines is None:
            max_lines = current_app.config.get('LOG_MONITOR_MAX_LINES', 1000)
            
        log_file = current_app.config.get('LOG_MONITOR_FILE')
        
        if not log_file or not os.path.exists(log_file):
            return {
                'content': f"日志文件不存在: {log_file}",
                'file_path': log_file,
                'file_size': 0,
                'last_modified': None,
                'exists': False,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        # 获取文件信息
        file_stats = os.stat(log_file)
        file_size = file_stats.st_size
        last_modified = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        # 读取日志内容（从文件末尾开始读取指定行数）
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                # 从文件末尾读取指定行数
                lines = f.readlines()
                if max_lines and len(lines) > max_lines:
                    lines = lines[-max_lines:]
                content = ''.join(lines)
        except Exception as e:
            content = f"读取日志文件出错: {str(e)}"
            
        return {
            'content': content,
            'file_path': log_file,
            'file_size': file_size,
            'last_modified': last_modified,
            'exists': True,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def tail_log(max_lines=None, follow=False, interval=None):
        """
        实时监控日志文件（类似tail -f）
        
        Args:
            max_lines: 最大返回行数
            follow: 是否持续监控
            interval: 监控间隔(秒)
            
        Yields:
            dict: 包含日志内容、文件信息的字典
        """
        if max_lines is None:
            max_lines = current_app.config.get('LOG_MONITOR_MAX_LINES', 1000)
        
        if interval is None:
            interval = current_app.config.get('LOG_MONITOR_UPDATE_INTERVAL', 5)
        
        log_file = current_app.config.get('LOG_MONITOR_FILE')
        
        if not follow:
            yield LogMonitor.get_log_content(max_lines)
            return
        
        # 文件不存在时的处理
        if not log_file or not os.path.exists(log_file):
            yield {
                'content': f"日志文件不存在: {log_file}",
                'file_path': log_file,
                'file_size': 0,
                'last_modified': None,
                'exists': False,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 等待文件出现
            while not os.path.exists(log_file):
                time.sleep(interval)
                yield {
                    'content': f"等待日志文件出现: {log_file}",
                    'file_path': log_file,
                    'file_size': 0,
                    'last_modified': None,
                    'exists': False,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        
        # 开始持续监控
        last_size = 0
        while True:
            result = LogMonitor.get_log_content(max_lines)
            current_size = result['file_size']
            
            # 文件大小发生变化才返回
            if current_size != last_size:
                yield result
                last_size = current_size
            
            time.sleep(interval) 