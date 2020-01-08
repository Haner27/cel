from model.mysql import BaseModel, Column, String, DATETIME


class Task(BaseModel):
    ASYNC_TASK = 'ASYNC'
    PERIODIC_TASK = 'PERIODIC'
    TASK_TYPE = [
        (ASYNC_TASK, '异步任务'),
        (PERIODIC_TASK, '定时任务')
    ]

    PRE_PUBLISH = 'PRE_PUBLISH'
    POST_PUBLISH = 'POST_PUBLISH'
    PRE_RUN = 'PRE_RUN'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    STATUS = [
        (PRE_PUBLISH, '发布前'),
        (POST_PUBLISH, '发布后'),
        (PRE_RUN, '执行前'),
        (SUCCESS, '执行成功'),
        (FAILURE, '执行失败')
    ]

    task_id = Column(String(100), nullable=False, index=True)
    type = Column(String(20), nullable=False)
    queue = Column(String(100), nullable=False)
    module = Column(String(100), nullable=False)
    func = Column(String(200), nullable=False)
    args = Column(String(500))
    kwargs = Column(String(500))
    status = Column(String(100), nullable=False)
    result = Column(String(500))
    exception = Column(String(1000))
    pre_publish_at = Column(DATETIME, default=None)
    post_publish_at = Column(DATETIME, default=None)
    pre_run_at = Column(DATETIME, default=None)
    post_run_at = Column(DATETIME, default=None, index=True)
