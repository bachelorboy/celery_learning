# -*- coding=utf-8-*-
from celery_cluster.agent2 import *
from celery_cluster.agent import *

print '*' * 20, u'任务多线程', '*' * 20
r = multithread_task.apply_async(args=(50, 80), countdown=2, queue='machine1', routing_key='machine1')

while True:
    if r.ready():
        print r.status
        result = multithread_task.AsyncResult(r.id)
        print result.get()  # 没有返回值
        break

print '*' * 20, u'参数为自定义对象', '*' * 20
r1 = plusone.apply_async(queue='machine1', routing_key='machine1', retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
})
result = plusone.AsyncResult(r1.id)
print u"返回json数据:{}".format(result.get())

# 任务传递参数为自定义对象，返回值也为自定义对象
s = Student("cai",60)
s.print_score()
r6 = plus_object.apply_async(args=(s,), queue='machine1', routing_key='machine1')
print u"返回自定义对象:{}".format(r6.get())

print '*' * 20, u'自定义任务类', '*' * 20

square = MyTask()
r2 = square.apply_async(kwargs={'data': 9}, countdown=2, queue='machine2', routing_key='machine2')
print r2.get()
# s=Student("cai",25)
# r1=plusone.delay(s)
