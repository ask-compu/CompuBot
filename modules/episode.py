#!/usr/bin/env python
"""
episode.py - Phenny MLP Episodes Module

"""

import re
import web
import json
import string
import ast
import calendar
import time

class Grab(web.urllib.request.URLopener):
    def __init__(self, *args):
        self.version = 'Mozilla/5.0 (CompuBot)'
        web.urllib.request.URLopener.__init__(self, *args)
        self.addheader('Referer', 'https://github.com/sbp/phenny')
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        return web.urllib.addinfourl(fp, [headers, errcode], "http:" + url)

def episode_find(query, phenny): 
    try:
        import dateutil.parser
    except:
        return 'error'
    query = query.replace('!', '')
    if re.compile('(?i)(season \d+(,)? episode \d+)').match(query):
        regex = re.compile('(?i)season (\d+)(?:,)? episode (\d+)')
        numbers = regex.findall(query)
        results = [int(i) for i in numbers[0]]
        snum = str(int(results[0]))
        enum = str(int(results[1]))
        uri = 'http://api.ponycountdown.com/' + snum + '/' + enum
        nl = query
    if re.compile('(?i)((s|se)\d+(, | |,)?(e|ep)\d+)').match(query):
        regex = re.compile('(?i)(?:s|se)(\d+)(?:, | |,)?(?:e|ep)(\d+)')
        numbers = regex.findall(query)
        results = [int(i) for i in numbers[0]]
        snum = str(int(results[0]))
        enum = str(int(results[1]))
        uri = 'http://api.ponycountdown.com/' + snum + '/' + enum
        nl = query
    if re.compile('(?i)next').match(query):
        uri = 'http://api.ponycountdown.com/next'
        nl = 'next'
    if re.compile('(?i)last').match(query):
        uri = 'http://api.ponycountdown.com/last'
        nl = 'last'
    rec_bytes = web.get(uri)
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    try:
        jsonstring[0]
    except:
        try:
            jsonstring['name']
        except:
            return 'nope$' + nl
    try:
        epname = jsonstring[0]['name']
        eps = str(jsonstring[0]['season'])
        epe = str(jsonstring[0]['episode'])
        etimeun = jsonstring[0]['time']
    except:
        epname = jsonstring['name']
        eps = str(jsonstring['season'])
        epe = str(jsonstring['episode'])
        etimeun = jsonstring['time']
    dt = dateutil.parser.parse(etimeun)
    timestamp1 = calendar.timegm(dt.timetuple())
    etimegmt = time.gmtime(timestamp1)
    etimeus = time.strftime('%A %B %d, %G at %I:%M:%S %p',etimegmt)
    if timestamp1 < time.time():
        return 'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' aired on ' + etimeus + ' GMT'
    if timestamp1 > time.time():
        return 'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' will air on ' + etimeus + ' GMT'
def episode(phenny, input): 
    """Finds MLP Episodes. Commands can be .ep season 2 episode 1 or .ep s2e1 or .ep next or .ep last"""
    query = input.group(2)
    if not query: return phenny.reply('.ep what?')

    uri = episode_find(query, phenny)
    if uri: 
        if uri.startswith('nope'):
            uris = uri.split('$')
            return phenny.say("Sorry " + input.nick + ", I couldn't find the " + uris[1] + " episode.")
        if uri.startswith('error'):
            return phenny.say('Please install dateutil with "pip install python-dateutil" and then say CompuBot: reload episode')
        else:
            phenny.say("Here's what I got, " + input.nick + ": " + uri)
            if not hasattr(phenny.bot, 'last_seen_uri'):
                phenny.bot.last_seen_uri = {}
            phenny.bot.last_seen_uri[input.sender] = uri
    else: phenny.say("Sorry " + input.nick + ", I couldn't find any episodes for '%s'." % query)
episode.commands = ['ep','episode']

if __name__ == '__main__': 
    print(__doc__.strip())
