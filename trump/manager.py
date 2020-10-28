#!/usr/bin/env python3
import sys, asyncio
from inspect import getmembers, isfunction, getfullargspec

from . import _commands


loop = asyncio.get_event_loop()
functions_list = {o[0]:o[1] for o in getmembers(_commands) if isfunction(o[1])}

try:
    import commands
    functions_list.update({o[0]:o[1] for o in getmembers(commands) if isfunction(o[1])})
except:
    #print("no custom commands")
    pass

def show_help(*args):
    for fn in sorted(functions_list):
        if not fn.startswith('_'):
            f = functions_list[fn]
            usage = '\nUse:\n%s' % f.__doc__.strip('\n') if f.__doc__ else ''
            args = '\nArg: %s' % ' '.join([f'[{x}]' for x in getfullargspec(f).args]) if getfullargspec(f).args else ''
            print("Cmd:", fn.replace('_', ' '), args, usage)
            print()


def main():
    import sys
    import inspect
    #print(f"{__name__}:OK")
    #print(sys.argv)
    cmd = '_'.join(sys.argv[1:3]) if len(sys.argv) > 1 else 'HELP'
    func = functions_list.get(cmd, show_help)
    argspec = getfullargspec(func)
    args = sys.argv[3:len(argspec.args)+3] if len(sys.argv) > 3 else []
    missed_args = len(argspec.args) - len(args)
    for i in range(missed_args):
        args.append(None)
    if asyncio.iscoroutinefunction(func):
        loop.run_until_complete(func(*args))
    else:
        func(*args)


if __name__ == '__main__':
    main()
