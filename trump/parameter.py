# auto load config
def main():
    import etcd3 
    import json
    import os
    from ._utils import _get_config_info
    #cwd = os.path.dirname(os.path.abspath(__file__))

    #files = os.listdir(cwd)

    #for i in files:
    #    if not i.startswith('_') and i.endswith('.py'):
    #        m = '.' + i[:-3]
    #        # get a handle on the module
    #        mdl = importlib.import_module(m, __package__)

    #        # is there an __all__?  if so respect it
    #        if "__all__" in mdl.__dict__:
    #            names = mdl.__dict__["__all__"]
    #        else:
    #            # otherwise we import all names that don't begin with _
    #            names = [x for x in mdl.__dict__ if not x.startswith("_")]

    #        # now drag them in
    #        globals().update({k: getattr(mdl, k) for k in names})
    #        globals().pop(i[:-3])
    config_url = os.environ.get('CONFIG_URL','127.0.1.1:2379/configs').strip()
    conn_info, path = _get_config_info(config_url)
    client = etcd3.client(**conn_info)
    kv = {}
    for v, meta in client.get_prefix(path):
        key = meta.key.split(b'/')[-1].decode('utf8').upper()
        if key.startswith("PARAMETER_"):
            if os.environ.get('TRUMP_CONFIG_IGNORE_ERROR', 'False') == 'True':
                try:
                    kv[key] = json.loads(v)
                except:
                    print(f'WWW: config error: key: {meta.key}')
            else:
                kv[key] = json.loads(v)

    globals().update(kv)
    from threading import Thread
    t = Thread(target=_watch_etcd, args=(client, path, _g_update))
    t.start()


def _watch_etcd(client, path, f):
    # watch prefix
    events_iterator, cancel = client.watch_prefix(path)
    import os
    import json
    for event in events_iterator:
        kv = {}
        key = event.key.split(b'/')[-1].decode('utf8').upper()
        if key.startswith("PARAMETER_"):
            if os.environ.get('TRUMP_CONFIG_IGNORE_ERROR', 'False') == 'True':
                try:
                    kv[key] = json.loads(event.value)
                except:
                    print(f'WWW: config error: key: {event.key}')
            else:
                kv[key] = json.loads(event.value)
            f(kv)
    cancel()


def _g_update(kv):
    globals().update(kv)


main()
globals().pop('main')
globals().pop('_watch_etcd')
globals().pop('_g_update')
