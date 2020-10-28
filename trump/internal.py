import aiohttp
import asyncio
from trump import log
import inspect

logger = log.Logger(__name__)

# await internal.call(uuid, MJMH_INTERNAL_JST, 'order_cancel', {'order_id': xx})
async def call(uuid, url, func, data):
    uuid = uuid if uuid else '-'
    async with aiohttp.ClientSession() as session:
        async with session.post(url+func, json=data) as response:
            result = await response.json()
            if not result or result.get("return_code") != "0000":
                await logger.err(uuid, inspect.currentframe().f_code.co_name + '.exception', {'url': url, 'func': func, 'data': data, 'result': result})
                raise Exception
            else:
                return result
