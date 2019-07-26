# -*- coding=utf-8-*-
from .maincelery import app
from celery import Task
from celery.utils.log import get_task_logger
from celery_once import QueueOnce
import time
from .multi import prinfo, SumThread
from multiprocessing import Pool

logger = get_task_logger(__name__)


class CountTask(Task):
    count = 0

    def on_success(self, retval, task_id, args, kwargs):
        self.count += 1
        return self.count


# 绑定上下文
@app.task(base=CountTask)
def send(self):
    if send.count <= 10:
        logger.info(('Executing task id{0.id},args:{0.args!r}'
                     'kwargs:{0.kwargs!r}').format(self.request))
        return 'Hello World'
    else:
        return 'end'


# graceful=True表示遇到重复方法时静默处理 AlreadyQueue异常
@app.task(base=QueueOnce, once={'graceful': True})
def add(x, y):
    time.sleep(2)
    return {'the value is': str(x + y)}


@app.task
def writefile():
    out = open('/home/caifaming/celery_cluster.txt', 'w')
    out.write('hello' + '\n')
    out.close()


@app.task
def getl(stri):
    return getlength(stri)


def getlength(stri):
    return len(stri)


# 创建任务的第二种方法 注册基于类的任务
class MyTask(Task):
    name = 'mytask'

    # 任务执行成功后调用 on_success
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("task id:{},arg:{},successful!".format(task_id, args))
        print u'执行成功!'

    # 任务执行失败后调用 on_failure
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("task id:{},arg:{},failed! errors:{}".format(task_id, args, exc))

    # 任务已经重试执行后调用 on_retry
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print u"任务已重试"
        logger.info("task id:{},arg:{},retried! einfo:{}".format(task_id, args, exc))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print u"任务返回后执行"

    def run(self, *args, **kwargs):
        x = kwargs.get('data', None)
        print x ** 2


# MyTask.bind(app)
# 注册任务
app.tasks.register(MyTask())
# mm=MyTask()
# r=mm.delay(data=2)  或者 r=mm.apply_async(kwargs={'data':4})
