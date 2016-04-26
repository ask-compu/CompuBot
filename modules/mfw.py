#!/usr/bin/env python

from urllib.parse import quote as urlquote
from urllib.parse import quote_plus as urlquoteplus
from urllib.error import HTTPError
import web
import json
from random import choice

def mlfw(phenny, input):
    """.mlfw <query> - My Little Face When: reaction images with ponies!
    Multiple tags should be separated by commas
    """
    q = input.group(2)
    if not q:
        phenny.say(mlfw.__doc__.strip())
        return
    try:
        req = web.get('http://mylittlefacewhen.com/api/v3/face/?tags__all={0}&order_by=-id&format=json'.format(urlquote(q)), isSecure=False)
    except (HTTPError, IOError):
        phenny.say("Oopsie, looks like the Internet is broken")
        return
    
    results = json.loads(req)

    if len(results['objects']) <= 0:
        phenny.say('I have no face for that')
        return

    try:
        object = choice(results['objects'])
        link = 'http://mlfw.info/f/{0}/'.format(object['id'])
        image = 'http://mlfw.info{0}'.format(object['image'])
        imgtitle = object['title']
    except AttributeError:
        phenny.say('No face for that')
        return
    
    phenny.say('Here ya go ' + input.nick + ': ' + imgtitle + ' - ' + image)

mlfw.commands = ('mlfw', 'mfw')

def dawg(phenny, input):
    """http://knowyourmeme.com/memes/xzibit-yo-dawg (.dawg <1>, <2>) I heard you like <1> so I put a <1> in your <1> so you can <2> while you <2>"""
    q = input.group(2)
    if q:
        words = q.split(', ')
    else:
        return phenny.say("I need 1 or 2 phrases dawg")
    if words[0].endswith('s'):
        wordss = words[0] + 'es'
    else:
        wordss = words[0] + 's'
    if len(words) > 1:
        phenny.say("Yo dawg")
        phenny.say("I heard you like " + wordss)
        phenny.say("So I put a " + words[0] + " in your " + words[0] + " so you can " + words[1] + " while you " + words[1])
    elif len(words) == 1:
        phenny.say("Yo dawg")
        phenny.say("I heard you like " + wordss)
        phenny.say("So I put a " + words[0] + " in your " + words[0] + " so you can " + words[0] + " while you " + words[0])
    else:
        return phenny.say("I need 1 or 2 phrases dawg")
dawg.commands = ['dawg']
