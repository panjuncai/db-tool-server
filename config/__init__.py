from .config import config

def get_config(config_name='default'):
    """
    获取配置类
    :param config_name: 配置名称，可选值：development, production, default
    :return: 配置类
    """
    return config.get(config_name, config['default'])
