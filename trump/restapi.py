import sys
import inspect

from sanic import Sanic, Blueprint
from sanic.response import json, text, HTTPResponse

from . import default_processor
from .utils import ok, fail
from trump import log


bp = Blueprint('restapi')

app = None

logger = log.Logger(__name__)


async def user_loader(app, request):
    request['user'] = request.get('session', {}).get('user')


async def _process(method, app, request, name, *args, **kargs):
    if app.views.get(name) and hasattr(app.views.get(name), method):
        # pre process
        func = getattr(app.views.get(name), method)
        if hasattr(func, 'login_required') and getattr(func, 'login_required') == False:
            pass
        else:
            if not request.get('user'):
                return fail('Not login.', status=401)
        result = await func(app, request, *args)
        if isinstance(result, HTTPResponse):
            return result
        # default process
        table_name = getattr(app.views.get(name), '__table__', name)
        kargs['table_name'] = table_name
        if table_name not in app.tables: return fail('404 no such table', status=404)
        try:
            result = await getattr(default_processor, method)(app, request, name, *args, **kargs)
            # post process
            post_proc = getattr(app.views.get(name), 'post_' + method, None)
            if post_proc:
                post_kargs = kargs.copy()
                post_kargs.pop('table_name')
                post_result = await post_proc(app, request, result, *args, **post_kargs)
                if post_result:
                    if isinstance(post_result, HTTPResponse): 
                        return post_result
                    else:
                        result = post_result
            if not result and method == 'get':
                return fail(status=404)
            #
            return ok(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return fail(traceback.format_exc())
    else:
        return fail('404 not found', status=404)


method_processor_dir = {
    'GET': 'ls',
    'POST': 'post',
}

method_processor_item = {
    'GET': 'get',
    'PUT': 'put',
    'DELETE': 'delete',
}

async def _proc(request, name, oid=None):
    response = None
    #
    if request.method == 'OPTIONS':
        func = getattr(app.views.get(name), 'options', None)
        if func:
            response = await func(app, request)
        else:
            response = text(None)
    #
    elif not oid and request.method in method_processor_dir:
        response = await _process(method_processor_dir.get(request.method),
                app, request, name)
    elif oid and request.method in method_processor_item:
        response = await _process(method_processor_item.get(request.method),
                app, request, name, oid)
    #
    return response if response else fail('Not impl.', status=400)


@bp.route(f'/<name>', methods=['GET', 'POST', 'OPTIONS'])
async def process_dir(request, name):
    return await _proc(request, name)


@bp.route(f'/<name>/<oid>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
async def process_item(request, name, oid):
    return await _proc(request, name, oid)


@bp.middleware('request')
async def load_user(request):
    uuid = request.get('uuid')
    if user_loader:
        await user_loader(app, request)
    await logger.info(uuid, inspect.currentframe().f_code.co_name, request.get('user'))
