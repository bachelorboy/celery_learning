# -*- coding=utf-8-*-
from celery_cluster.agent2 import *
from celery_cluster.agent import *

# 测试 celery_once
# 不过当开启ack_late之后，如果执行add任务的一个进程突然退出，则该任务不会再此执行，即使worker恢复正常
r = add.apply_async(args=(12, 27), queue='machine1', routing_key='machine1')
r = add.apply_async(args=(12, 27), queue='machine1', routing_key='machine1')  # 无结果 同一任务只能执行一次
#
# while True:
#     if r.ready():
#         print r.get()
#         break
#
# # 任务未继承 celery_once,发现相同任务被执行两次
# r1 = say.apply_async(args=('Good afternoon!',), queue='machine1', routing_key='machine1')
# r1 = say.apply_async(args=('Good afternoon!',), queue='machine1', routing_key='machine1')
# time.sleep(2)
# print r1.status
# print r1.get()

r3=div.apply_async(args=(2, 0), queue='machine2', routing_key='machine2')


