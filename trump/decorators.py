import functools
from sanic.response import json, text


def set_option(request, k, v):
    #if not 'options' in request.keys():
    if not request.get('options'):
        request['options'] = {}
    request['options'][k] = v


def login_required(required):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.login_required = required
        return wrapper
    return decorator


def anonymous(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        return func(*args, **kw)
    wrapper.login_required = False
    return wrapper


def no_pager(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        set_option(args[1], 'pager', False)
        return func(*args, **kw)
    return wrapper


def table_headers(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        set_option(args[1], 'table_headers', True)
        return func(*args, **kw)
    return wrapper


def cors(origins):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            set_option(args[1], 'cors_headers', origins)
            return func(*args, **kw)
        wrapper.cors_headers = origins
        return wrapper
    return decorator
