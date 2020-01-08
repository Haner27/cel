*mac
*python3

1.安装docker:
brew cask install docker

2.点击"小鲸鱼"启动docker服务

3.安装python依赖包:
pip install -r requestment

4.启动mysql,rabbitmq服务：
    *所用到的依赖服务mysql,rabbitmq都是使用docker容器来支持，只是想快速的在本地跑起来，也方便大家可以使用
    4.1.修改server文件夹下mysql.sh， rabbitmq.sh执行权限：
    chmod +x mysql.sh rabbitmq.sh

    4.2.执行启动mysql,rabbitmq服务：
    ./mysql.sh
    ./rabbitmq.sh
    * mysql -h 127.0.0.1:5000 -u root -p 123456     这里在宿主机开放的端口3306，用户名root, 密码123456
    * rabbitmq开放宿主机端口5672和15672，其中5672是服务端口，15672是管理服务端口。管理服务页面：http://127.0.0.1:15672,用户名guest, 密码guest

5.创建mysql数据库cel：
    5.1.连接mysql：
    mysql -h 127.0.0.1:5000 -u root -p 123456

    5.2.创建数据库cel：
    create database cel;

6.根据model创建任务日志表task：
    在工程目录下执行：
    python create_table.py

7.在task目录下定义异步执行的方法：
    * 参考task/test_task.py

8.开启celery worker:
    例：celery worker -A mq.celery_app -Q mq --autoscale=5,3 -n mq -l info -E

9.在test.py文件里调用定义好的异步执行的方法：
    * 参考test.py

10.mysql数据库中cel库中task表，记录任务流转状态。