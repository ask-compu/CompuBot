#!/usr/bin/env python
"""
admin.py - Phenny Admin Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re

def join(phenny, input): 
    """Join the specified channel. This is an admin-only command."""
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): 
        return
    if input.admin: 
        channel, key = input.group(1), input.group(2)
        if not key: 
            phenny.write(['JOIN'], channel)
        else: 
            phenny.write(['JOIN', channel, key])
join.rule = r'\.join (#\S+)(?: *(\S+))?'
join.priority = 'low'
join.example = '.join #example or .join #example key'

def autojoin(phenny, input): 
    """Join the specified channel when invited by an admin."""
    if input.admin: 
        channel = input.group(1)
        phenny.write(['JOIN'], channel)
autojoin.event = 'INVITE'
autojoin.rule = r'(.*)'

def part(phenny, input): 
    """Part the specified channel. This is an admin-only command."""
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): 
        return
    if input.admin: 
        # TODO: add optional arguments for a part message
        phenny.write(['PART'], input.group(2).strip())
part.commands = ['part']
part.priority = 'high'
part.example = '.part #example'

def quit(phenny, input): 
    """Quit from the server. This is an owner-only command."""
    # Can only be done in privmsg by the owner
    if input.sender.startswith('#'): 
        return
    if input.owner: 
        # TODO: add optional arguments for a quit message
        phenny.write(['QUIT'])
        __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'high'

def msg(phenny, input): 
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): 
        return
    a, b = input.group(2), input.group(3)
    if (not a) or (not b): 
        return
    if input.admin: 
        phenny.msg(a, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.priority = 'low'

def me(phenny, input): 
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): 
        return
    if input.admin: 
        msg = '\x01ACTION {0}\x01'.format(input.group(3))
        phenny.msg(input.group(2), msg)
me.rule = (['me'], r'(#?\S+) (.*)')
me.priority = 'low'

'''
def silence(phenny, input):
    def ishostmask(subject):
        to_match = '(.*)!(.*)@(.*)'
        return re.compile(to_match).match(subject)
    # Can only be done in privmsg by an admin
    if input.sender.startswith('#'): 
        phenny.say('Nuh uh! Not here you can\'t!')
        return
    if input.admin:
        silence = 'SILENCE'
        if input.group(2) not in ('+','-'):
            phenny.msg(input.sender, 'Come on, plus or minus! Add or remove! You know this!')
        else:
            if input.group(2) is '+':
                #add to the silence list
                silence = silence + ' +'
            elif input.group(2) is '-':
                #remove from the silence list
                silence = silence + ' -'
            if input.group(3):
                #discard everything after the first space
                mask_to_silence = input.group(3).partition(' ')[0]
                phenny.msg(input.sender, "I'll be ignoring this (" + input.group(3).partition(' ')[2] + 
                    ") extra bit. Follow the rules and Auntie Pinkie will take care of everything else!")
                if ishostmask(mask_to_silence):
                    silence = silence + mask_to_silence + ' a'
                    phenny.msg(input.sender, '"' + silence + '" is being sent to the server')
                else:
                    phenny.msg(input.sender, 'That\'s not a hostmask, silly!')
        phenny.msg(input.sender, input.group(2) + ' group 2 input')
        phenny.msg(input.sender, input.group(3) + ' group 3 input')
silence.rule = (['silence'], r'(#?\S+) (.+)')
silence.priority = 'high'
silence.example = '.silence + foo!bar@buzz.com to add a silence or .silence - fizz!bang@widgets.net to remove a silence'
'''

if __name__ == '__main__': 
    print(__doc__.strip())
