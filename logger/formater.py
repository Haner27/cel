from logging import Formatter

__author__ = 'nengfang.han'

# 默认日志格式
DEFAULT_LOG_FORMAT = '[%(name)s][%(levelname)s][%(asctime)s]%(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_FORMAT = Formatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT)

# 访问日志格式
ACCESS_LOG_FORMAT = '[%(name)s][%(levelname)s][%(asctime)s] ip:%(ip)s app_key:%(app_key)s method:%(method)s url:%(url)s status:%(status)s\n' +\
                    'parameters:\n%(params)s'
ACCESS_FORMAT = Formatter(ACCESS_LOG_FORMAT, DEFAULT_DATE_FORMAT)

# 错误日志格式
ERROR_LOG_FORMAT = '[%(name)s][%(levelname)s][%(asctime)s] ip:%(ip)s app_key:%(app_key)s method:%(method)s url:%(url)s\n' +\
                   'parameters:\n%(params)s\nerror:\n%(message)s\n-- %(filename)s line:%(lineno)d'
ERROR_FORMAT = Formatter(ERROR_LOG_FORMAT, DEFAULT_DATE_FORMAT)

# SOCKET日志格式
SOCKET_LOG_FORMAT = '%(json_data)s'
SOCKET_FORMAT = Formatter(SOCKET_LOG_FORMAT)