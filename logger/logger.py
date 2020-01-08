from logging import Logger, Formatter, INFO, StreamHandler, ERROR, WARNING
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler, SocketHandler

from .handler import KafkaHandler
from .filter import MineLogFilter, KafkaFilter
from .formater import DEFAULT_FORMAT, ACCESS_FORMAT, ERROR_FORMAT
from conf import conf

__author__ = 'nengfang.han'

DEFAULT_MAIL_HOST = ('smtp.126.com', 25)
DEFAULT_FILTER = MineLogFilter()


class MineLogger(Logger):
    def __init__(self, name, level=None, formatter=None, default_filter=DEFAULT_FILTER):
        # 初始化父类
        super(MineLogger, self).__init__(name)

        # 默认formatter
        self.formatter = formatter or DEFAULT_FORMAT

        # 默认level
        self.level = level or INFO

        # 默认filter
        if default_filter:
            self.default_filter = default_filter
            self.addFilter(self.default_filter)

        # 默认log_path
        self.log_path = '{0}.log'.format(self.name)

    def add_stream_handler(self, level=None, formatter=None, filters=None):
        handler = StreamHandler()
        handler.setLevel(level or self.level)
        handler.setFormatter(formatter or self.formatter)

        if filters is None:
            filters = []
        for f in filters:
            handler.addFilter(f)
        self.addHandler(handler)
        return self

    def add_rotating_handler(self, log_path=None, level=None, max_bytes=10 * 1024 * 1024, backup_count=5,
                             formatter=None, filters=None):
        handler = RotatingFileHandler(log_path or self.log_path, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(level or self.level)
        handler.setFormatter(formatter or self.formatter)
        self.addHandler(handler)

        if filters is None:
            filters = []
        for f in filters:
            handler.addFilter(f)
        return self

    def add_timed_rotating_handler(self, log_path=None, level=None, when='D', interval=1, backup_count=5,
                                   formatter=None, filters=None):
        handler = TimedRotatingFileHandler(log_path or self.log_path, when=when, interval=interval,
                                           backupCount=backup_count)
        handler.setLevel(level or self.level)
        handler.setFormatter(formatter or self.formatter)

        if filters is None:
            filters = []
        for f in filters:
            handler.addFilter(f)
        self.addHandler(handler)
        return self

    def add_smtp_handler(self, from_addr, to_addrs, subject, mail_host=None, username=None, password=None, level=None,
                         formatter=None, filters=None):
        handler = SMTPHandler(mailhost=mail_host or DEFAULT_MAIL_HOST, fromaddr=from_addr, toaddrs=to_addrs,
                              subject=subject, credentials=(username, password))
        handler.setLevel(level or self.level)
        handler.setFormatter(formatter or self.formatter)

        if filters is None:
            filters = []
        for f in filters:
            handler.addFilter(f)
        self.addHandler(handler)
        return self

    def add_kafka_handler(self, kafka_url, topic, level=None, formatter=None, filters=None):
        handler = KafkaHandler(kafka_url, topic)
        handler.setLevel(level or self.level)
        handler.setFormatter(formatter or self.formatter)

        if filters is None:
            filters = []
        for f in filters:
            handler.addFilter(f)
        self.addHandler(handler)
        return self


# 常规日志
cel_logger = MineLogger('cel', default_filter=DEFAULT_FILTER)
cel_logger.add_stream_handler()
cel_logger.add_timed_rotating_handler(conf.log.mq_log_path)
cel_logger.add_timed_rotating_handler(conf.log.mq_log_err_path, level=ERROR)
# if Config.STAGE.lower() == 'pro':
#     # 上线后才打点
#     cel_logger.add_kafka_handler(
#         kafka_url=conf.kafka.url,
#         topic=conf.kafka.topic,
#         filters=[KafkaFilter()]
#     )
