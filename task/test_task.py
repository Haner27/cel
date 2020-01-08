from mq import celery_app
from time import sleep

from task import CallbackTask

__author__ = 'nengfang.han'


@celery_app.task(bind=True, queue='mq')
def add(self, x, y):
    """
    当使用 bind=True 参数之后, 函数的参数发生变化, 多出了参数 self, 这这相当于把 div 编程了一个已绑定的方法,
    通过 self 可以获得任务的上下文.
    # todo: 进度条实现
    """
    sleep(3)
    return x + y


@celery_app.task(queue='mq')
def right(x, y):
    sleep(3)
    return x - y


@celery_app.task(queue='mq')
def fail(x, y):
    sleep(3)
    a = 1 / 0
    return x - y


