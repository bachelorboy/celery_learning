celery demo
===========

python + celery + redis + rabbitmq

## 目录结构

    ├── celery_cluster
    │   ├── __init__.py
    │   ├── agent2.py
    │   ├── agent.py
    │   ├── config.py
    │   ├── maincelery.py
    │   └── multi.py
    ├── Test2.py
    └── TEST.py


## 介绍
broker采用rabbitmq, backend采用redis
两个任务模块agent.py, agent2.py, 配置文件config.py.   
包含异步任务, 定时任务   
若任务参数传递自定义对象, 则任务序列化方式只能是pickle;   
任务中自定义多线程   
用到了celery-once确保一个任务只能执行一次, celery-once采用redis分布式锁实现

#### 测试代码:  
    TEST.py, Test2.py

## 启动worker命令:  
    celery -A celery_cluster.maincelery worker  -P prefork -c 3 -l info  -O fair -Q machine1 -n worker2@%h
    
    -A: 指定创建的celery对象的位置，该app.celery_tasks.celery指的是app包下面的celery_tasks.py模块的celery实例
        ,注意一定是初始化后的实例，后面加worker表示该实例就是任务执行者;

    -Q: 指的是该worker接收指定的队列的任务，这是为了当多个队列有不同的任务时可以独立；如果不设会接收所有的队列的任务;
    -l: 指定worker输出的日志级别;
    -P: 并发类型(prefork(多进程),eventlet(协程),gevent)
    -c: 并发数量
    -n: worker名字
    
    
    
## 启动定时任务任务:  
    celery beat -A celery_cluster.maincelery
