import os

import pyaml

CONF_FILE = 'cel.yaml'


class Conf:
    def __init__(self, conf_filename):
        # 自定义的配置
        self.path = self.PathConf()

        # 加载yaml里的配置
        self.yaml_obj = self.load_conf_from_yaml(conf_filename)
        self.stage = self.yaml_obj.get('stage').lower()
        self.log = self.LogConf(self.yaml_obj.get('log-dir'), work_dir=self.path.work_dir)
        self.rabbitmq = self.RabbitMQConf(self.yaml_obj.get('rabbitmq'))
        self.mysql = self.MysqlConf(self.yaml_obj.get('mysql'))
        self.kafka = self.KafkaConf(self.yaml_obj.get('kafka'))

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
        def __init__(self, log_dir, work_dir):
            self.log_dir = log_dir
            if not self.log_dir.startswith('/'):
                self.log_dir = os.path.join(work_dir, log_dir)
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

    class KafkaConf:
        # kafka 配置
        def __init__(self, kafka_conf):
            self.topic = kafka_conf['topic']
            self.url = kafka_conf['url']


conf = Conf(CONF_FILE)