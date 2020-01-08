from mq import celery_app
from time import sleep
from task import CallbackTask

__author__ = 'nengfang.han'


# 消息得决定发往的exchange和自己带有的routing_key
@celery_app.task(
    bind=True,
    queue='mq'
)
def add(self, x, y):
    """
    当使用 bind=True 参数之后, 函数的参数发生变化, 多出了参数 self, 这这相当于把 div 编程了一个已绑定的方法,
    通过 self 可以获得任务的上下文.
    # todo: 进度条实现
    """
    sleep(3)
    return x + y


@celery_app.task(
    bind=True,
    queue='mq'
)
def div(self, x, y):
    sleep(1)
    return x / y


@celery_app.task(
    exchange='fans',
    routing_key='celery'
)
def right(x, y):
    sleep(3)
    return x - y


@celery_app.task(
    exchange='topic',
    routing_key='topic.job'
)
def fail(x, y):
    sleep(3)
    a = 1 / 0
    return x - y


