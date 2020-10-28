import os
import asyncio
import json
from ._utils import _get_config_info


SPACE = " "*4


def test_add(x:int,y:dict=2):
    if not x:
        pass
    print(x+y)
    pass


async def show_tables():
    '''
    show tables
    '''
    from pprint import pprint
    loop = asyncio.get_event_loop()
    from trump.query import create_pools, get_all_tables
    from trump.config import DB_CONFIG
    pool = await create_pools(loop, **DB_CONFIG)
    tables = await get_all_tables(pool, DB_CONFIG['db'])
    pprint(tables)


async def run_sql(sql):
    '''
    run sql
    '''
    from pprint import pprint
    loop = asyncio.get_event_loop()
    from trump.query import create_pools, query
    from trump.config import DB_CONFIG
    if not sql.split()[0].upper() == 'SELECT':
        print("Error on support `SELECT`")
    else:
        pool = await create_pools(loop, **DB_CONFIG)
        pprint(await query(pool, sql))


def _load_config_from_file(fn):
    kv = {}
    k = ''
    v = ''
    with open(fn) as f:
        n = 1
        for line in f.readlines():
            if line.startswith('+') or line.startswith('-'):
                raise Exception(f"Error config file `{fn}' at line {n}")
            if line.startswith(f'{SPACE}'):
                v += line.strip()
            else:
                if v:
                    kv[k] = json.dumps(json.loads(v))
                v = ''
                k = line.strip()
            n+=1
        else:
            kv[k] = json.dumps(json.loads(v))
        return kv


def _load_config_from_etcd(config_url):
    import etcd3
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    kv = {}
    for v, meta in client.get_prefix(path):
        k = meta.key.split(b'/')[-1].decode('utf8').upper()
        v = json.dumps(json.loads(v.decode('utf8')))
        kv[k] = v
    return kv


def config_list(config_url):
    '''
    <url>
    '''
    import etcd3
    kv ={}
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    for v, meta in client.get_prefix('/'):
        k = meta.key.decode('utf8')
        #v = json.dumps(json.loads(v.decode('utf8')))
        v = v.decode('utf8')
        print(meta, k, f"'{v}'")


def config_dump(config_url):
    kv = _load_config_from_etcd(config_url)
    for k in kv:
        print(k)
        for line in kv[k].splitlines():
            print(f'{SPACE}{line}')


def config_load(config_url, config_file, real_run=False):
    '''
    '''
    import etcd3
    #import config_dev
    #from config import config
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    configs = _load_config_from_file(config_file)

    for i in configs:
        k, v = (f'{path}{i.lower()}', configs[i])
        print(k, v)
        if real_run:
            client.put(k, v)


def config_diff(config_url1, config_url2, diff_only=False):
    '''
    config_url1 config_url2 <1|2>
       1: all diff 
       2: only add or del
    '''
    diff_type = diff_only if diff_only else '1'
    from pprint import pprint
    kvs = []
    kv_all = {}
    for i, config_url in enumerate((config_url1, config_url2)):
        kvs.append({})
        if config_url.find(':') != -1:
            kv = _load_config_from_etcd(config_url)
        else:
            kv = _load_config_from_file(config_url)
        for k in kv:
            kvs[i][k] = kv[k]
            kv_all[k] = kv[k]

    for k in kv_all:
        if kvs[0].get(k) == kvs[1].get(k):
            if not diff_only:
                print(k.upper())
                for line in kvs[0][k].splitlines():
                    print(f'{SPACE}{line}')
        else:
            rm =  ''
            add = ''
            for line in kvs[0].get(k, '').splitlines():
                rm = f'-{SPACE}{line}'
            for line in kvs[1].get(k, '').splitlines():
                add = f'+{SPACE}{line}'
            if diff_type in ('0', '1'):
                print(f"{k.upper()}")
                if rm: 
                    print(rm)
                if add:
                    print(add)
            else:
                if not all((rm, add)):
                    if rm: 
                        print(f"-{k.upper()}")
                        print(rm)
                    if add:
                        print(f"+{k.upper()}")
                        print(add)


def config_delete(config_url, key):
    import etcd3
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    print(client.delete(path + key))

def config_put(config_url, key, value):
    import etcd3
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    print('todo')
    #print(client.delete(path + key))


def view():
    '''
    list view
    '''
    for i in os.walk('views'):
        paths = i[0].split('/')
        if i[0] == 'views':
            for j in i[2]:
                print(f'={j}')
        elif len(paths) == 2 and not paths[-1].endswith('__pycache__'):
            for j in i[2]:
                print(f'-{paths[1]}/{j}')


def view_create(view, options, table_name):
    if os.path.exists(os.path.join('views', view+'.py')):
        print('exists')
    else:
        print('todo')
