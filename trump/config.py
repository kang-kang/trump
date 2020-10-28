import logging
df = '%Y-%m-%d %H:%M:%S'
FORMAT = '[%(asctime)s.%(msecs)03d000] \033[31m(%(name)s)[%(process)d] [%(levelname)s] %(message)s\033[0m'
logging.basicConfig(format=FORMAT, datefmt=df)
log = logging.getLogger(__name__)
# auto load config
def main():
    import json
    import os
    from ._utils import _get_config_info, _load_config_from_file
    #from .log_sync import warning as warning, err
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
    kv = {}
    if os.environ.get('CONFIG_URL'):
        import etcd3 
        config_url = os.environ.get('CONFIG_URL','127.0.1.1:2379/configs').strip()
        conn_info, path = _get_config_info(config_url)
        client = etcd3.client(**conn_info)
        for v, meta in client.get_prefix(path):
            if os.environ.get('TRUMP_CONFIG_IGNORE_ERROR', 'False') == 'True':
                try:
                    kv[meta.key.split(b'/')[-1].decode('utf8').upper()] = json.loads(v)
                except:
                    log.warning(f'WWW: config error: key: {meta.key}')
            else:
                kv[meta.key.split(b'/')[-1].decode('utf8').upper()] = json.loads(v)
    elif os.path.exists('config.txt'):
        kv.update(_load_config_from_file('config.txt'))
    else:
        log.error('Warning: no config file or config url')
    globals().update(kv)


main()
globals().pop('main')
