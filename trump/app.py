import logging
import pkgutil
import uuid
import traceback
import json
from pprint import pprint
import inspect
import platform

from trump import log

import aioredis 

from sanic import Sanic
from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound
#from sanic_session import Session, InMemorySessionInterface, RedisSessionInterface
from sanic_session import Session, AIORedisSessionInterface

from . import restapi
from .query import create_pools, get_all_tables

import views
from .config import DB_CONFIG

df = '%Y-%m-%d %H:%M:%S'

FORMAT = '[%(asctime).%(msecs)03d] \033[33m%(message)s\033[0m'
FORMAT = '[%(asctime)s.%(msecs)03d000] \033[32m(%(name)s)[%(process)d] [%(levelname)s] %(message)s\033[0m'
logging.basicConfig(format=FORMAT, datefmt=df)
logger = logging.getLogger(__name__)


class Trump(Sanic):

    def getBlueprints(self):
        print(self.blueprints)

import sanic
logging_config = sanic.log.LOGGING_CONFIG_DEFAULTS.copy()

logging_config['formatters']['generic']['datefmt'] = df
logging_config['formatters']['access']['datefmt'] = df
logging_config['formatters']['generic']['format'] = '[%(asctime)s.%(msecs)03d000] \033[33m(%(name)s)[%(process)d] [%(levelname)s] %(message)s\033[0m'
logging_config['formatters']['access']['format'] = '[%(asctime)s.%(msecs)03d000] - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d'

app = Trump(log_config=logging_config)

route = app.route
static = app.static
listener = app.listener

restapi.app = app
bp = restapi.bp.route
middleware = restapi.bp.middleware


restapi.bp.name = 'trump'
url_prefix = None
session_name = None
session_enable = True


@app.listener('before_server_start')
async def register_db(app, loop):
    # session
    logger.warning("session_enable %s" % session_enable)
    if session_enable:
        session = Session()
        try:
            from .config import REDIS_CONFIG
        except:
            REDIS_CONFIG = {'host': 'localhost', 'port': 6379}
        app.redis = await aioredis.create_redis_pool((REDIS_CONFIG['host'], REDIS_CONFIG['port']), password=REDIS_CONFIG.get('password'))
        import os
        domain = os.environ.get('TRUMP_DOMAIN')
        if not session_name:
            cookie_name = "session_%s" % url_prefix.replace('/', '_') if url_prefix else 'session_id'
        else:
            cookie_name = session_name
        print(cookie_name, domain)
        session.init_app(app, interface=AIORedisSessionInterface(app.redis, cookie_name=cookie_name, domain=domain))

    # db
    app.pool = await create_pools(loop, **DB_CONFIG)
    app.tables = await get_all_tables(app.pool, DB_CONFIG.get('db'))
    app.table_schema = DB_CONFIG.get('db')
    app.views = {}
    for importer, modname, ispkg in pkgutil.iter_modules(views.__path__):
        m = importer.find_module('views.' + modname).load_module('views.' + modname)
        if not ispkg:
            app.views[modname] = m
        else:
            app.views[modname] = m
            for sub_importer, sub_modname, _ in pkgutil.iter_modules(m.__path__):
                sub_m = sub_importer.find_module('views.' + 
                        modname + '.' + sub_modname).load_module('views.' + 
                                modname + '.' + sub_modname)
                app.views[ modname + '_' + sub_modname] = sub_m
    count = 0
    for view in app.views:
        _table = getattr(app.views[view], '__table__', None)
        with_table = " with table `%s'" % _table if _table else ''
        for method in dir(app.views[view]):
            if method in ['ls', 'get', 'post', 'delete', 'put']:
                func = getattr(app.views[view], method)
                post_func = getattr(app.views[view], f"post_{method}", None)
                post_f = ''
                if post_func:
                    post_f = '#'
                login_required = ''
                if hasattr(func, 'login_required') and getattr(func, 'login_required') == False:
                    login_required = '@'
                count +=1
                logger.warning(f"register `%s:{login_required}%s{post_f}' using `%s'%s" %
                    (view, method, app.views[view].__name__, with_table))
    logger.warning("total register %s interfaces" % count )


# class Redis:
#     """
#     A simple wrapper class that allows you to share a connection
#     pool across your application.
#     """
#     _pool = None
# 
#     async def get_redis_pool(self):
#         REDIS_CONFIG = {'host': 'localhost', 'port': 6379}
#         try:
#             from .config import REDIS_CONFIG
#         except:
#             pass
#         if not self._pool:
#             self._pool = await asyncio_redis.Pool.create(
#                 host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], password=REDIS_CONFIG.get('password'), poolsize=10
#             )
# 
#         return self._pool
# 
#     async def close(self):
#         if self._pool:
#             self._pool.close()


#redis = Redis()


@app.listener('before_server_stop')
async def server_stop(app, loop):
    #await redis.close()
    if getattr(app, 'redis'):
        app.redis.close()
        await app.redis.wait_closed()


@app.middleware('request')
async def add_uuid(request):
    request['uuid'] = uuid.uuid4().hex


@app.middleware('request')
async def log_on_request(request):
    uuid = request.get('uuid')
    try:
        body = request.body.decode('utf8')
    except:
        try:
            if request.headers.get('content-type').startswith('multipart/form-data'):
                body = ["MULTIPART/FORM-DATA", request.form, request.files.keys()]
            else:
                try:
                    body = str(request.body)
                except:
                    body = "BODY ERROR"
        except:
            body = "MULTIPART BODY ERROR"
    finally:
        await log.info(uuid, 'request', {'method': request.method,
            'url': request.url, 
            'headers': list(request.headers.items()),
            'body': body})


@app.middleware('response')
async def log_on_response(request, response):
    uuid = request.get('uuid')
    try:
        body = json.loads(response.body.decode('utf8'))
    except:
        try:
            body = response.body.decode('utf8')
        except:
            body = str(response.body)
    await log.info(uuid, 'response.header', list(response.headers.items()))
    #await log.info(uuid, 'response.body_truncated', body)
    await log.info(uuid, 'response.body', body)

@app.exception(NotFound)
async def ignore_404s(request, exception):
    uuid = request.get('uuid')
    await log.warning(uuid, 'exception', f'404 `{request.url}` not found')
    return response.json({"status": "404"}, status=404)

async def server_error_handler(request, exception):
    uuid = request.get('uuid')
    await log.err(uuid, 'exception', traceback.format_exc())
    return response.json({"status": "error"}, status=500)


app.error_handler.add(Exception, server_error_handler)


def run(*args, **kargs):
    global app
    if not session_name:
        cookie_name = "session_%s" % url_prefix.replace('/', '_') if url_prefix else 'session_id'
    else:
        cookie_name = session_name
    #if session_enable:
    #    Session(app, interface=RedisSessionInterface(redis.get_redis_pool, cookie_name=cookie_name))
    if url_prefix:
        restapi.bp.url_prefix = url_prefix
    app.blueprint(restapi.bp)
    run_args = {'host': '0.0.0.0', 'port': 9000, 'debug': True, 'auto_reload': platform.system() == 'Linux', 'access_log': False}
    run_args.update(kargs)
    logger.warning("Serve at http://%s:%s%s" %
            (run_args['host'], run_args['port'], url_prefix if url_prefix else '/'))
    return app.run(**run_args)
