import os
import pkgutil

from celery import Celery

from conf import conf, celery_conf
import task_hook  # 加载hook方法

__author__ = 'nengfang.han'

"""
mq包：用于异步消息队列
"""


def get_tasks_module_paths(package_name, package_path, tasks_module_paths=None):
    if tasks_module_paths is None:
        tasks_module_paths = []

    for _, name, is_pkg in pkgutil.iter_modules(package_path):
        if is_pkg:
            child_package_name = '{}.{}'.format(package_name, name)
            child_package_path = [os.path.join(package_path[0], name)]
            get_tasks_module_paths(child_package_name, child_package_path, tasks_module_paths)
        else:
            tasks_module_paths.append('{}.{}'.format(package_name, name))

    return tasks_module_paths


celery_app = Celery(
    'cel',
    include=get_tasks_module_paths(
        package_name='task',
        package_path=[conf.path.celery_task_dir]
    )
)
celery_app.config_from_object(celery_conf)
