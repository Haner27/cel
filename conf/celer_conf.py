from kombu import Exchange, Queue
from kombu.common import Broadcast

from conf import conf


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
    CELERY_DEFAULT_QUEUE = 'mq'

    def queue_name_list(self):
        return [q.name for q in self.CELERY_QUEUES]


celery_conf = CeleryConf()