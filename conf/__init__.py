import os

import pyaml
from kombu import Exchange, Queue
from kombu.common import Broadcast

CONF_FILE = 'cel.yaml'


class Conf:
    def __init__(self, conf_filename):
        # 自定义的配置
        self.path = self.PathConf()

        # 加载yaml里的配置
        self.yaml_obj = self.load_conf_from_yaml(conf_filename)
        self.stage = self.yaml_obj.get('stage').lower()
        self.log = self.LogConf(self.yaml_obj.get('log-dir'))
        self.rabbitmq = self.RabbitMQConf(self.yaml_obj.get('rabbitmq'))
        self.mysql = self.MysqlConf(self.yaml_obj.get('mysql'))

    def load_conf_from_yaml(self, conf_filename):
        yaml_file = os.path.join(self.path.config_dir, conf_filename)  # 配置文件地址
        with open(yaml_file) as f:
            yaml = pyaml.yaml.safe_load(f)
        return yaml

    class PathConf:
        # 路径相关配置
        def __init__(self):
            self.work_dir = os.path.dirname(os.path.dirname(__file__))
            self.config_dir = os.path.join(self.work_dir, 'conf')
            self.celery_task_dir = os.path.join(self.work_dir, 'task')

    class LogConf:
        # 日志配置
        def __init__(self, log_dir):
            self.log_dir = log_dir
            self.mq_log_path = os.path.join(self.log_dir, 'mq.log')
            self.mq_log_err_path = os.path.join(self.log_dir, 'mq-err.log')

    class RabbitMQConf:
        # rabbitmq 配置
        def __init__(self, rabbit_mq_conf):
            self.url = rabbit_mq_conf['url']

    class MysqlConf:
        # mysql 配置
        def __init__(self, mysql_conf):
            self.db = mysql_conf['db']
            self.url = mysql_conf['url']


conf = Conf(CONF_FILE)


class CeleryConf:
    BROKER_URL = conf.rabbitmq.url  # 中间人
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 180000}

    CELERYD_MAX_TASKS_PER_CHILD = 200
    CELERY_IGNORE_RESULT = True
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_ACKS_LATE = True
    CELERYD_PREFETCH_MULTIPLIER = 1

    # 定义exchange
    EX_MQ = Exchange('mq', type='direct')
    EX_FAN = Exchange('fans', type='fanout')
    EX_TOPIC = Exchange('topic', type='topic')

    # 定义queue
    CELERY_QUEUES = (
        Queue('mq', exchange=EX_MQ, routing_key='mq'),
        Queue('fan-1', exchange=EX_FAN),
        Queue('fan-2', exchange=EX_FAN),  # 绑定同一个fanout模式的exchange的queue,都会收到消息
        Broadcast(name='fan-3', exchange=EX_FAN),  # 广播模式，监听同一个Broadcast队列的所有worker都能收到消息
        Queue('topic-1', exchange=EX_TOPIC, routing_key='topic.*'),
        Queue('topic-2', exchange=EX_TOPIC, routing_key='#.job')
    )


    def queue_name_list(self):
        return [q.name for q in self.CELERY_QUEUES]


celery_conf = CeleryConf()