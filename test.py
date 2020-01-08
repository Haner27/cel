def test_async():
    from task.test_task import fail, right, add, div
    # add.delay(100, y=99)
    # div.delay(100, 2)
    fail.delay(100, y=2)
    # right.delay(27, y=2)
    # div.delay(100, 0)


if __name__ == '__main__':
    test_async()

    # direct exchange 测试使用
    # celery worker -A mq.celery_app -Q mq --autoscale=5,3 -n mq -l info -E

    # fanout exchange 和 broadcast queue测试使用
    # celery worker -A mq.celery_app -Q fan-1 --autoscale=5,3 -n fan-1 -l info -E
    # celery worker -A mq.celery_app -Q fan-2 --autoscale=5,3 -n fan-2 -l info -E
    # celery worker -A mq.celery_app -Q fan-2 --autoscale=5,3 -n fan-2.1 -l info -E
    # celery worker -A mq.celery_app -Q fan-3 --autoscale=5,3 -n fan-3 -l info -E
    # celery worker -A mq.celery_app -Q fan-3 --autoscale=5,3 -n fan-3.1 -l info -E

    # topic exchange 测试使用
    # celery worker -A mq.celery_app -Q topic-1 --autoscale=5,3 -n topic-1 -l info -E
    # celery worker -A mq.celery_app -Q topic-2 --autoscale=5,3 -n topic-2 -l info -E
