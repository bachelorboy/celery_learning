# -*- coding=utf-8-*-
from .maincelery import app
import time
from celery.schedules import crontab
from celery import Task
from .multi import prinfo, SumThread
from celery.utils.log import get_task_logger
from multiprocessing import Pool

logger = get_task_logger(__name__)


@app.task
def multithread_task(low, high):
    # pool=Pool()
    # p=pool.map(prinfo, [[1, 2], [3, 4], [5, 6]])
    # p.close()
    # p.join()
    thread1 = SumThread(0, low)
    thread2 = SumThread(low, high)
    thread2.start()
    thread1.start()
    thread1.join()
    thread2.join()
    result = thread1.total + thread2.total
    print "result=", result


class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print '%s:%s' % (self.name, self.score)

# 自定义对象序列化方式只能为pickle
@app.task
def plus_object(s):
    s.score += 1
    print "new score:{}".format(s.score)
    # return {"name":s.name,"score":s.score}  #  也可以用返回json数据
    return s  # 可以返回自定义对象，但是序列化方式只能是pickle


@app.task(bind=True, serializer='json', default_retry_delay=300, max_retries=5)
def plusone(self):
    s = Student("cai", 18)
    print 'original score:{}'.format(s.score)
    try:
        s.score += 1
        print "socre plus one:{}".format(s.score)
    except Exception as e:
        raise self.retry(exc=e)
    finally:
        return {"name": s.name, "score": s.score}
    # return s # 报错


# u''' celery 4.0以后才有的周期性调用函数的定时功能 '''
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # 每10秒执行say(Hello Everybody!)
#     sender.add_periodic_task(10.0, say.s('Hello Everybody!'), name='hello')
#
#     # 每周一 7：30 a.m.执行 say('Happy Mondays')
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         say.s('Happy Mondays!'),
#     )


@app.task
def say(arg):
    time.sleep(10)
    print arg
    return arg


@app.task(bind=True)
def div(self, x, y):
    logger.info(('Executing task id{0.id},args:{0.args!r}'
                 'kwargs:{0.kwargs!r}').format(self.request))
    # 当分母为0时，每5秒就会重试一次，一共重试3次，然后抛出异常
    try:
        result = x / y
    except ZeroDivisionError as e:
        print u'分母不为0'
        raise self.retry(exc=e, countdown=2, max_retries=3, interval_step=0.2)  # countdown指定多少秒后执行任务
    return result
