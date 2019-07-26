# -*- coding=utf-8-*-
from kombu import Queue,Exchange
from kombu.serialization import registry
from kombu import serialization
from datetime import timedelta

BROKER_URL = 'amqp://localhost//'
# 不要用rabbitmq作为backend,因为rabbitmq会为每个任务结果创建一个队列,导致队列越来越多(不确定)
CELERY_RESULT_BACKEND = 'amqp://localhost//'
# CELERY_RESULT_BACKEND = 'redis://localhost'
CELERY_TASK_RESULT_EXPIRES = 3600  # 任务结果超时时间
CELERY_TASK_SERIALIZER = 'pickle'  # 任务序列化方式
CELERY_RESULT_SERIALIZER = 'pickle' # 任务执行结果序列化方式
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'application/text']

CELERY_DEFAULT_DELIVERY_MODE = 'transient'  # 队列和消息持久化

# 一个worker其实就是一个工作池,比如进程池，worker每次抓取(multiplier*并发数)条消息
CELERYD_PREFETCH_MULTIPLIER = 1  # celery worker 每次去rabbitmq取任务的数量

# CELERY_IGNORE_RESULT = False
# worker在任务执行完之后确认
CELERY_ACKS_LATE = True  # 开启ack应答,任务执行完则worker向broker发送应答信号,broker再删除队列中的消息
CELERY_TRACK_STARTED = True  # worker执行任务时，任务更性状态为已启动
CELERYD_MAX_TASKS_PER_CHILD = 200  # 每个worker子进程执行了多少次任务后会挂掉，主要是释放资源，防止内存泄漏

# 导入任务模块
CELERY_IMPORTS = {
  'celery_cluster.agent',
  'celery_cluster.agent2',
}

CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

# delivery=1表示消息不会持久化到磁盘,2 表示消息会持久化到磁盘
# durable=True 表示队列持久化
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('machine1', Exchange('agent', delivery_mode=2), routing_key='machine1', durable=True),
    Queue('machine2', Exchange('agent'), routing_key='machine2'),
)

CELERY_ROUTES = {
    'celery_cluster.agent.add': {  # agent.add的消息会进入default队列
        'queue': 'default',
        'routing_key': 'default',
    },
}
# 定时任务
CELERYBEAT_SCHEDULE = {
    'add': {
        'task': 'celery_cluster.agent.add',
        'schedule': timedelta(seconds=5),
        'args': (16, 2),  # 任务函数参数
    },
}
