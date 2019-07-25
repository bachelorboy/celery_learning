# -*- coding=utf-8-*-
from celery import Celery
from celery_once import QueueOnce

app = Celery('myapp', include=['celery_cluster.agent', 'celery_cluster.agent2'])

app.config_from_object('celery_cluster.config')

# app.conf.ONCE = {
#     'backend': 'celery_once.backends.Redis',
#     'settings': {
#         'url': 'redis://localhost:6379/0',
#         'default_timeout': 60*60,
#     }
# }

# celery_once(0.1.4版本支持celery 3.1)
# 同一时间一个任务只能执行一次(采用redis分布式锁实现)
app.conf.ONCE_REDIS_URL = 'redis://localhost:6379/0'
app.conf.ONCE_DEFAULT_TIMEOUT = 60 * 60

if __name__ == '__main__':
    app.start()
