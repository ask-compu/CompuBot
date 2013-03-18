#!/usr/bin/env python
"""
info.py - Phenny Information Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def doc(phenny, input): 
    """Shows a command's documentation, and possibly an example."""
    name = input.group(1)
    name = name.lower()

    if name in phenny.doc: 
        phenny.reply(phenny.doc[name][0])
        if phenny.doc[name][1]: 
            phenny.say('e.g. ' + phenny.doc[name][1])
doc.rule = ('$nick', '(?i)(?:help|doc) +([A-Za-z]+)(?:\?+)?$')
doc.example = '$nickname: doc tell?'
doc.priority = 'low'

def commands(phenny, input): 
    # This function only works in private message
    if input.sender.startswith('#'): return
    names = ', '.join(sorted(phenny.doc.keys()))
    phenny.say('Commands I recognise: ' + names + '.')
    phenny.say(("For help, do '%s: help example?' where example is the " + 
                    "name of the command you want help for.") % phenny.nick)
commands.commands = ['commands']
commands.priority = 'low'

def help(phenny, input): 
    phenny.say("Hey there, I'm a friendly bot for this channel. Say \".commands\" " +
        "to me in private. My owner is {0}.".format(phenny.config.owner))
help.commands = ['help']
help.priority = 'low'

def stats(phenny, input): 
    """Show information on command usage patterns."""
    commands = {}
    users = {}
    channels = {}

    ignore = set(['f_note', 'startup', 'message', 'noteuri', 'logger',
        'snarfuri', 'measure', 'messageAlert'])
    for (name, user), count in list(phenny.stats.items()): 
        if name in ignore: continue
        if not user: continue

        if not user.startswith('#'): 
            try: users[user] += count
            except KeyError: users[user] = count
        else: 
            try: commands[name] += count
            except KeyError: commands[name] = count

            try: channels[user] += count
            except KeyError: channels[user] = count

    comrank = sorted([(b, a) for (a, b) in commands.items()], reverse=True)
    userank = sorted([(b, a) for (a, b) in users.items()], reverse=True)
    charank = sorted([(b, a) for (a, b) in channels.items()], reverse=True)

    # most heavily used commands
    creply = 'most used commands: '
    for count, command in comrank[:10]: 
        creply += '%s (%s), ' % (command, count)
    phenny.say(creply.rstrip(', '))

    # most heavy users
    reply = 'power users: '
    for count, user in userank[:10]: 
        reply += '%s (%s), ' % (user, count)
    phenny.say(reply.rstrip(', '))

    # most heavy channels
    chreply = 'power channels: '
    for count, channel in charank[:3]: 
        chreply += '%s (%s), ' % (channel, count)
    phenny.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'

if __name__ == '__main__': 
    print(__doc__.strip())
