from datetime import datetime
import aiomysql

from trump.query import *

import logging.config



log = logging.getLogger(__name__)

def _fix_types(record, attributes):
    d = {}
    for i in record:
        if attributes.get(i) == FIELD_TYPE.TIMESTAMP:
            # prc = pytz.timezone('PRC')
            # d[i] = record[i].astimezone(prc).strftime("%Y-%m-%d %H:%M:%S")
            if record[i]:
                d[i] = record[i].strftime("%Y-%m-%d %H:%M:%S")
        elif attributes.get(i) == FIELD_TYPE.DATETIME:
            if record[i]:
                d[i] = record[i].strftime("%Y-%m-%d %H:%M:%S")
        elif attributes.get(i) == FIELD_TYPE.DECIMAL:
            if record[i]:
                d[i] = record[i].strftime("%Y-%m-%d %H:%M:%S")
        else:
            d[i] = record[i]
    return d


async def query(pool, sql, *args, fetch_type = 'fetch', uuid='-', uid='-'):
    async with pool.acquire() as connection:
        async with connection.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql,(*args,))
            attributes = {s[0]: s[1] for s in cur.description}
            if fetch_type == 'fetch':
                result = await cur.fetchall()
                return [_fix_types(item, attributes) for item in result]
            elif fetch_type == 'fetchrow':
                result = await cur.fetchone()
                if result:
                    return _fix_types(result, attributes)
            elif fetch_type == 'fetchval':
                result = await cur.fetchone()
                result = list(result.values())[0]
                if type(result) == datetime:
                    return result.strftime("%Y-%m-%d %H:%M:%S")
                return result
            elif fetch_type == 'attributes':
                return {s[0]: 'text' for s in cur.description}


async def execute(pool, sql, *args, table, uuid='-', uid='-'):
    async with pool.acquire() as connection:
        statement = await connection.prepare(sql.format(*range(1, sql.count('{}')+1)))
        updestmt = await connection.prepare("SELECT * FROM %s"%(table))
        attributes = {s[0]: s[1][1] for s in updestmt.get_attributes()}
        values = _prepare_vaules(updestmt, args)
        log.debug(f"{uuid} {uid} arg:{args}\nsql:{sql}\nval:{values}")
        result = await connection.fetch(sql, *values)