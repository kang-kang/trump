import os
import sys
import json
from datetime import datetime
import socket
import time
from urllib.parse import urlparse

import requests
from redis import Redis

from trump import config


HOST = os.environ.get('SERVER', socket.gethostname())
ENV = os.environ.get('ENV', 'development')
PRJ = os.environ.get('SUPERVISOR_PROCESS_NAME', sys.argv[0])

'''
level name and code

Value 	Severity 	Keyword 	Deprecated keywords 	Description 	Condition
0 	Emergency 	emerg 	panic[7] 	System is unusable 	A panic condition.[8]
1 	Alert 	alert 		Action must be taken immediately 	A condition that should be corrected immediately, such as a corrupted system database.[8]
2 	Critical 	crit 		Critical conditions 	Hard device errors.[8]
3 	Error 	err 	error[7] 	Error conditions
4 	Warning 	warning 	warn[7] 	Warning conditions
5 	Notice 	notice 		Normal but significant conditions 	Conditions that are not error conditions, but that may require special handling.[8]
6 	Informational 	info 		Informational messages
7 	Debug 	debug 		Debug-level messages 	Messages that contain information normally of use only when debugging a program.[8]
'''

LOG_HANDLERS = getattr(config, 'LOG_HANDLER', ['stdout'])
LOG_FILTER_REDIS = getattr(config, 'LOG_FILTER_REDIS', None)
LOG_FILTER_KEY = f'log_filter_{ENV}_{PRJ}'

def get_frame_info(level=2):
    current_frame = sys._getframe(level)
    debug = 0
    if debug: 
        #fn = current_frame.f_code.co_filename
        #line_no = current_frame.f_lineno
        for i in dir(current_frame):
             v = str(getattr(current_frame, i))
             print(i, f'{v[:80]}{"..." if len(v)>50 else ""}')
    return str(current_frame.f_code)


def _msg(level, module, uuid, tag, msg):
    try:
        json.dumps(msg)
    except:
        print(f'[{datetime.now():%Y-%m-%d %H:%M:%S.%f}] EEE {msg}')
        msg = str(msg)
    return {
            "level": level,
            "host":HOST,
            "env": ENV,
            "prj": PRJ,
            "time": time.time(), 
            "module": module,
            "tag": tag, 
            "uuid": uuid,
            "message": msg,
            }


def _post(url, msg):
    #url = 'http://localhost:9001'
    try:
        response = requests.post(url, json=msg)
        return response.text()
    except:
        pass


def _send(url, msg):
    try:
        msg = msg.copy() # new object for console, because datetime can't be jsonify
        msg['levelname'] = 'emerg,alert,crit,err,warning,notice,info,debug'.split(',')[msg['level']].upper()
        msg['message'] = str(msg.get('message'))
        conn_info = urlparse(url)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((conn_info.hostname, conn_info.port))
        s.send((json.dumps(msg)+'\n').encode())
        s.close()
    except Exception as e:
        print(f'[{datetime.now():%Y-%m-%d %H:%M:%S.%f}] EEE failed to send to `{url}: {e}`')

def _print(message):
    message = message.copy() # new object for console, because datetime can't be jsonify
    formater = '[{asctime:%Y-%m-%d %H:%M:%S.%f}] [{host}][{prj}][{env}] \033[36m[{module}]({tag}) [{levelname}] [{uuid}] {message}\033[0m'
    dt = datetime.fromtimestamp(int(message['time']))
    dt = dt.replace(microsecond=int(message['time']%1*1E6)) 
    message['asctime'] = dt
    message['levelname'] = 'emerg,alert,crit,err,warning,notice,info,debug'.split(',')[message['level']].upper()
    print(formater.format(**message))

ops = {
        'ge': lambda x, y: x >= y,
        'gt': lambda x, y: x > y,
        'le': lambda x, y: x <= y,
        'lt': lambda x, y: x < y,
        'eq': lambda x, y: x == y,
        'contains': lambda x, y: x in y,
        'nin': lambda x, y: x not in y,
        }
redis_info = urlparse(LOG_FILTER_REDIS)
print(redis_info)
redis = Redis(host=redis_info.hostname, port=6379 if not redis_info.port else redis_info.port)  
def get_log_filter():
    if LOG_FILTER_REDIS:
        val = redis.smembers(LOG_FILTER_KEY) 
        return (v.decode('utf8').split(',') for v in val)
    else:
        return []

def _log(*args): 
    message = _msg(*args)
    for flt in get_log_filter():
        if ops.get(flt[1])(flt[2], message.get(flt[0])):
            return
    for log_handler in LOG_HANDLERS:
        if log_handler.startswith('tcp://'):
            _send(log_handler, message)
        elif log_handler.startswith('http'):
            _post(log_handler, message)
        elif log_handler == 'stdout':
            _print(message)


class Logger:
    def __init__(self, name='root'):
        self.name = name
    """
# below code was genareted by this code:
----
for level, levelname in enumerate('emerg,alert,crit,err,warning,notice,info,debug'.split(',')):
    print(f'''def {levelname}(self, *args, **kargs):
    _log({level}, self.name, *args, **kargs)
''')

for level, levelname in enumerate('emerg,alert,crit,err,warning,notice,info,debug'.split(',')):
    print(f'{levelname} = _logger.{levelname}')

''')
----
    """
    def emerg(self, *args, **kargs):
        _log(0, self.name, *args, **kargs)

    def alert(self, *args, **kargs):
        _log(1, self.name, *args, **kargs)

    def crit(self, *args, **kargs):
        _log(2, self.name, *args, **kargs)

    def err(self, *args, **kargs):
        _log(3, self.name, *args, **kargs)

    def warning(self, *args, **kargs):
        _log(4, self.name, *args, **kargs)

    def notice(self, *args, **kargs):
        _log(5, self.name, *args, **kargs)

    def info(self, *args, **kargs):
        _log(6, self.name, *args, **kargs)

    def debug(self, *args, **kargs):
        _log(7, self.name, *args, **kargs)


_logger = Logger()
emerg = _logger.emerg
alert = _logger.alert
crit = _logger.crit
err = _logger.err
warning = _logger.warning
notice = _logger.notice
info = _logger.info
debug = _logger.debug

if __name__ == '__main__':
    debug('-', 'trump.log', f'LOG_FILTER_KEY is `{LOG_FILTER_KEY}`')
