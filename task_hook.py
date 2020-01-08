import json
import traceback

from celery.signals import before_task_publish, after_task_publish, task_prerun, task_postrun, task_failure

from model.mysql import session_cxt
from model.mysql.task import Task
from util.datetime import now

"""各个阶段的时间处理器"""


@before_task_publish.connect
def before_task_publish_handler(body=None, **kwargs):
    """
    任务发布前回调处理器
    """
    try:
        with session_cxt() as s:
            task = Task()

            task.task_id = kwargs['headers']['id']
            task_name = kwargs['headers']['task']
            args = kwargs['headers']['argsrepr']
            func_kwargs = kwargs['headers']['kwargsrepr']
            task.type = Task.ASYNC_TASK
            queue_name = kwargs['declare'][0].name
            if queue_name.find('schedule') >= 0:
                task.type = Task.PERIODIC_TASK
            last_dot_index = task_name.rfind('.')
            task.module = task_name[0: last_dot_index]
            task.func = task_name[last_dot_index + 1:]
            task.args = str(args)
            task.kwargs = str(func_kwargs)
            task.queue = queue_name
            task.pre_publish_at = now()
            task.status = Task.PRE_PUBLISH

            s.add(task)
    except Exception as e:
        print(traceback.format_exc(e))  # todo: 记录日志


@after_task_publish.connect
def after_task_publish_handler(body=None, **kwargs):
    """
    任务发布后回调处理器
    """
    try:
        task_id = kwargs['headers']['id']
        with session_cxt() as s:
            task = s.query(Task).filter(Task.task_id == task_id).first()
            if task:
                task.post_publish_at = now()
                task.status = Task.POST_PUBLISH
                s.add(task)
    except Exception as e:
        print(traceback.format_exc(e))  # todo: 记录日志


@task_prerun.connect
def task_pre_run_handler(task_id=None, task=None, args=None, **kwargs):
    """
    任务在worker端开始执行前回调，在worker进程中执行该回调
    """
    try:
        with session_cxt() as s:
            task = s.query(Task).filter(Task.task_id == task_id).first()
            if task:
                task.pre_run_at = now()
                task.status = Task.PRE_RUN
                s.add(task)
                print('[PRE_RUN]{}'.format(task.task_id if task else ''))
    except Exception as e:
        print(traceback.format_exc(e))  # todo: 记录日志


@task_postrun.connect
def task_post_run_handler(task_id=None, task=None, args=None, state=None, retval=None, **kwargs):
    """
    任务在worker端执行完后回调，在worker进程中执行该回调
    """
    try:
        with session_cxt() as s:
            task = s.query(Task).filter(Task.task_id == task_id).first()
            if task:
                if retval is None:
                    retval = ''

                task.post_run_at = now()
                if state == 'SUCCESS':
                    task.status = Task.SUCCESS
                    task.result = json.dumps(retval, ensure_ascii=False)
                else:
                    task.status = Task.FAILURE
                    task.exception = str(retval)

                s.add(task)
                print('[{}]{}'.format(task.status, task.task_id if task else ''))
    except Exception as e:
        print(traceback.format_exc(e))  # todo: 记录日志