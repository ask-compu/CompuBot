#!/usr/bin/env python
"""
reload.py - Phenny Module Reloader Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import sys, os.path, time, imp
import irc

home = os.getcwd()

def f_reload(phenny, input): 
    """Reloads a module, for use by admins only.""" 
    if not input.admin: return

    name = input.group(2)
    if name == phenny.config.owner: 
        return phenny.reply('What?')

    if (not name) or (name == '*'): 
        phenny.variables = None
        phenny.commands = None
        phenny.setup()
        return phenny.reply('done')

    path = None

    if name not in sys.modules: 
        filename = os.path.join(home, 'modules', name)
        filenamepy = os.path.join(home, 'modules', name+'.py')
        if os.path.isfile(filename):
            phenny.reply('%s: found new module!' % name)
            path = filename
        elif os.path.isfile(filenamepy):
            phenny.reply('%s: found new module!' % name)
            path = filenamepy
        else:
            return phenny.reply('%s: no such module!' % name)

    # Thanks to moot for prodding me on this
    if not path:
        path = sys.modules[name].__file__
    if path.endswith('.pyc') or path.endswith('.pyo'): 
        path = path[:-1]
    if not os.path.isfile(path): 
        return phenny.reply('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'): 
        module.setup(phenny)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    phenny.register(vars(module))
    phenny.bind_commands()

    phenny.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'high'
f_reload.thread = False

def c_reload(phenny, input):
    """Reloads config, for use by admins only."""
    if not input.admin: return

    attr = input.group(2)
    if attr == phenny.config.owner: 
        return phenny.reply('What?')
        
    name = os.path.basename(phenny.config.filename).split('.')[0] + '_config'
    module = imp.load_source(name, phenny.config.filename)
    if not hasattr(module,attr):
        return phenny.say("I don't see %s in config"%(attr))
    
    setattr(phenny.config,attr,getattr(module,attr))
    phenny.say("%s loaded"%(attr))
        
c_reload.name = 'creload'
c_reload.rule = ('$nick', ['creload'], r'(\S+)?')
c_reload.priority = 'high'
c_reload.thread = False

if __name__ == '__main__': 
    print(__doc__.strip())
