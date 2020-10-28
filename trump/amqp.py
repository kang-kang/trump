import aiohttp
import json
from trump.config import MSG_URL


async def send(queue, msg=None, headers=None,  delay=0, persistent=True, msg_url=MSG_URL, uuid=None):
    async with aiohttp.ClientSession() as session:
        async with session.post(msg_url, json={
            'headers': headers,
            'message': msg,
            'delay': delay,
            'persistent': persistent,
            'queue': queue,
            }) as resp:
            print(await resp.text())
    if True:
        return {"return_code": "0000", "return_msg": "success"}
    else:
        return {"return_code": "1111", "return_msg": "failure"}


def send_sync():
    pass
