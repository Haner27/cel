def test_async():
    from task.test_task import fail, right
    fail.delay(1, y=2)
    right.delay(1, y=2)


if __name__ == '__main__':
    test_async()