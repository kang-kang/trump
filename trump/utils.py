import functools
from sanic.response import json, text


def ok(data=None, total=None, table_headers=None, return_msg="成功!"):
    th = table_headers if table_headers else getattr(data, 'extras', {}).get('table_headers', {})
    tot = total if total!=None else getattr(data, 'total', -2)
    extras = getattr(data, 'extras', {})
    if isinstance(data, list):
        result = {"data": {"total": tot, "list": data, "extras": extras}, "status": 0,
                "return_code": "0000", "return_msg": return_msg}
        if th: result['table_headers'] = th
    elif data is None:
        result ={"data": data, "status": 0, "return_code": "0000", "return_msg": return_msg}
    else:
        result = {"data": data, "status": 0,
                "return_code": "0000", "return_msg": return_msg}
        if th: result['table_headers'] = th
        if extras: result['extras'] = extras
    return json(result)


def fail(data=None, return_code="1111", return_msg="错误!", status=200):
    if data is None:
        result =  {"data": data, "status": 1,
                "return_code": return_code, "return_msg": return_msg}
    else:
        result = {"data": data, "status": 1,
                "return_code": return_code, "return_msg": return_msg}
    return json(result, status=status)


def prepareRole(request, uid):
    return rolename in request.get('user', {}).get('roles', [])

def checkRole(request, uid, roles):
    return rolename in request.get('user', {}).get('roles', [])

def hasRole(request, rolename):
    return rolename in request.get('user', {}).get('roles', [])


def isLogin(request):
    if request.get('user'):
        return request.get('user', {}).get('id')
    else:
        return False


def get_uuid(request):
    return request.get('uuid', '-')


def get_uid(request):
    return request.get('user', {}).get('uid', '-')


def uuid_info(request):
    user = request.get('user') if request.get('user') else {}
    return {'uuid': request.get('uuid', '-'), 'uid': user.get('uid', '-')}
