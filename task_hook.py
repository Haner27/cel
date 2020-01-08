import json
import traceback

from celery.signals import before_task_publish, after_task_publish, task_prerun, task_postrun, task_failure

from logger.logger import cel_logger, cel_logger
from model.mysql import session_cxt
from model.mysql.task import Task
from util.datetime import now

"""各个阶段的时间处理器"""


@before_task_publish.connect
def before_task_publish_handler(body=None, **kwargs):
    """
    任务发布前回调处理器
    """
    task_id = kwargs['headers']['id']
    queue_name = kwargs['declare'][0].name
    try:
        with session_cxt() as s:
            task = Task()
            task.task_id = task_id
            task_name = kwargs['headers']['task']
            args = kwargs['headers']['argsrepr']
            func_kwargs = kwargs['headers']['kwargsrepr']
            task.type = Task.ASYNC_TASK
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
            cel_logger.info('[PRE_PUBLISH]task: {}'.format(task_id))
    except Exception as ex:
        cel_logger.error('[PRE_PUBLISH][EXCEPTION]task: {}\nexception: \n{}'.format(
            task_id, traceback.format_exc(ex))
        )


@after_task_publish.connect
def after_task_publish_handler(body=None, **kwargs):
    """
    任务发布后回调处理器
    """
    task_id = kwargs['headers']['id']
    try:
        with session_cxt() as s:
            task = s.query(Task).filter(Task.task_id == task_id).first()
            if task:
                task.post_publish_at = now()
                task.status = Task.POST_PUBLISH
                s.add(task)
                cel_logger.info('[POST_PUBLISH]task: {}'.format(task_id))
    except Exception as ex:
        cel_logger.error('[POST_PUBLISH][EXCEPTION]task: {}\nexception: \n{}'.format(task_id, traceback.format_exc(ex)))


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
                cel_logger.info('[PRE_RUN]task: {}'.format(task_id))
    except Exception as ex:
        cel_logger.error('[PRE_RUN][EXCEPTION]task: {}\nexception: \n{}'.format(task_id, traceback.format_exc(ex)))


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
                    cel_logger.info('[POST_RUN][{}]task: {}\nresult: {}'.format(task.status, task_id, task.result))
                else:
                    task.status = Task.FAILURE
                    task.exception = str(retval)
                    cel_logger.error('[POST_RUN][{}]task: {}\nexception: \n{}'.format(task.status, task_id, task.exception))

                s.add(task)
    except Exception as ex:
        cel_logger.error('[POST_RUN][EXCEPTION]task: {}\nexception: \n{}'.format(task_id, traceback.format_exc(ex)))