from functools import wraps
from uuid import uuid1
import time
from datetime import datetime
from threading import Thread
import pkgutil
import traceback
from inspect import getmembers, isfunction, getfullargspec

from crontab import CronTab


import tasks


def cron(crontab):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        __trump_task__ = hasattr(wrapper, '__trump_task__')
        if not __trump_task__:
            wrapper.__trump_task__ = []
        wrapper.__trump_task__.append(('cron', crontab))
        return wrapper
    return decorate


def repeat(repeat_time):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        __trump_task__ = hasattr(wrapper, '__trump_task__')
        if not __trump_task__:
            wrapper.__trump_task__ = []
        wrapper.__trump_task__.append(('repeat', repeat_time))
        return wrapper
    return decorate

def _runner(func, full_name):
    tid = uuid1().hex
    base = f"[{datetime.now()}]"
    print(f"{base}[RUN][{tid}] {full_name}")
    try:
        func()
    except Exception as e:
        print(f"{base}[ERR][{tid}] {full_name} {e}\n{traceback.format_exc()}")
    print(f"{base}[FIN][{tid}] {full_name}")

def _run_cron(full_name, func, cron):
    c = CronTab(cron)
    while True:
        time.sleep(c.next(default_utc=False))
        _runner(func, full_name)

def _run_repeat(full_name, func, repeat):
    first = True
    while True:
        now = time.time()
        if first:
            first = False
        else:
            if int(now) % repeat == 0:
                _runner(func, full_name)
        remainder = now % 1
        time.sleep(1.1-remainder)

 
def run():
    functions_list = {}
    for importer, modname, ispkg in pkgutil.iter_modules(tasks.__path__):
        m = importer.find_module('tasks.' + modname).load_module('tasks.' + modname)
        functions_list = [ (o[0], o[1]) for o in getmembers(m) if isfunction(o[1]) ]
        for fn, f in functions_list:
            if hasattr(f, '__trump_task__'):
                for x in f.__trump_task__:
                    full_name = f'{modname}.{fn}'
                    if x[0] == 'cron':
                        print(f"[{datetime.now()}][ADD][CRON] {full_name}/`{x[1]}'")
                        t = Thread(target=_run_cron, args=(full_name, f, x[1]))
                        t.start()
                    elif x[0] == 'repeat':
                        print(f"[{datetime.now()}][ADD][REPT] {full_name}/{x[1]}")
                        t = Thread(target=_run_repeat, args=(full_name, f, x[1]))
                        t.start()


if __name__ == '__main__':
    run()
