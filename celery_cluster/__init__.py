# -*- coding=utf-8-*-
u'''
master为任务分发节点,slave1为worker1,salve2为worker2

master :在celery_cluster同级目录
输入python命令进入python解释器
from celery_cluster.agent import add

res=add.apply_async(args=[122,34],queue='machine1',routing_key='machine1')
res.get()
slave1:celery -A celery_cluster.maincelery worker  -P prefork -c 4 -l info  -O fair -Q machine1 -n worker1@%h
salve2:celery -A celery_cluster.maincelery worker -l info -Q machine2

-A: 指定创建的celery对象的位置，该app.celery_tasks.celery指的是app包下面的celery_tasks.py模块的celery实例
,注意一定是初始化后的实例，后面加worker表示该实例就是任务执行者;

-Q: 指的是该worker接收指定的队列的任务，这是为了当多个队列有不同的任务时可以独立；如果不设会接收所有的队列的任务;
-l: 指定worker输出的日志级别;
-P: 并发类型(prefork(多进程),eventlet(协程),gevent)
-c: 并发数量
-n: worker名字

启动定时任务: celery beat -A celery_cluster.maincelery

'''


