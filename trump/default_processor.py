from sanic.response import json, text

from .utils import uuid_info, ok, fail
from .query import create_item, get_items, get_item, modify_item, delete_item, get_check_acl, get_table_header


class ListData(list):
    def __init__(self):
        self.extras = {}
        self.total = -1
        self.response = None

    def set_total(self, v):
        self.total = v

    def get_total(self):
        return self.total

    def set_extra(self, k, v):
        self.extras[k] = v

    def get_extra(self, k):
        return self.extras[k]



class DictData(dict):
    def __init__(self):
        self.extras = {}
        self.total = -1

    def set_extra(self, k, v):
        self.extras[k] = v

    def get_extra(self, k):
        return self.extras[k]


async def _set_table_headers(app, request, name, data):
    table_headers = []
    if request.get('options', {}).get("table_headers"):
        table_headers = await get_table_header(app.pool, name, app.table_schema)
    data.set_extra('table_headers', table_headers)


async def ls(app, request, name, table_name=None):
    total, data = await get_items(app.pool, table_name, request.args,
            with_total=True, pager=request.get('options', {}).get('pager', True), **uuid_info(request))
    _data = ListData()
    _data.extend(data)
    await _set_table_headers(app, request, table_name, _data)
    #data.extras['total'] = total
    #_data.set_extra('total', total)
    _data.set_total(total)
    return _data


async def get(app, request, name, oid, table_name = None):
    data = await get_item(app.pool, table_name, int(oid), **uuid_info(request))
    _data = DictData()
    _data.update(data if data else {})
    await _set_table_headers(app, request, table_name, _data)
    return _data


async def post(app, request, name, table_name = None):
    data = await create_item(app.pool, table_name, request.json, lock_table=False, **uuid_info(request))
    return data


async def put(app, request, name, oid, table_name = None):
    data = await modify_item(app.pool, table_name, oid, request.json, **uuid_info(request))
    return data


async def delete(app, request, name, oid, table_name = None):
    data = await delete_item(app.pool, table_name, oid, **uuid_info(request))
    return data
