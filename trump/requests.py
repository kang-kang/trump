from packaging import version
import httpx

async def _base(method, *args, **kargs):
    if version.parse(httpx.__version__) < version.parse('0.10.0'):
        async with httpx.Client() as client:
            return await getattr(client, method)(*args, **kargs)
    else:
        async with httpx.AsyncClient() as client:
            return await getattr(client, method)(*args, **kargs)

async def post(*args, **kargs):
    return await _base('post', *args, **kargs)

async def get(*args, **kargs):
    return await _base('get', *args, **kargs)

async def put(*args, **kargs):
    return await _base('put', *args, **kargs)

async def delete(*args, **kargs):
    return await _base('delete', *args, **kargs)
