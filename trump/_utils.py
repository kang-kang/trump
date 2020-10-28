import json

SPACE = " "*4

def _get_config_info(config_url):
    user = None
    password = None
    if '@' in config_url:
        user_password, config_url = config_url.split('@')
        user, password = user_password.split(':')
    host = config_url.split(':')[0]
    port = int(config_url.split('/')[0].split(':')[1])
    path = '/'+'/'.join((config_url.strip('/').split('/')[1:]))+'/'
    return {'user': user, 'password': password, 'host': host, 'port': port}, path


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
                    kv[k] = json.loads(v)
                v = ''
                k = line.strip()
            n+=1
        else:
            kv[k] = json.loads(v)
        return kv

