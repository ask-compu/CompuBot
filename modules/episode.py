#!/usr/bin/env python
"""
episode.py - Phenny MLP Episodes Module

"""

import re
import web
import json
import time

_re_full = re.compile('(?i)season (?P<season>\d+),? episode (?<episode>\d+)')
_re_short = re.compile('(?i)se?(?P<season>\d+),? ?ep?(?P<episode>\d+)')
_re_movie = re.compile('(?i)movie ?(?P<episode>\d+)')


def duration(seconds, _maxweeks=99999999999):
    return ', '.join('%d %s' % (num, unit)
             for num, unit in zip([(seconds // d) % m
                       for d, m in ((604800, _maxweeks), 
                                                        (86400, 7), (3600, 24), 
                                                        (60, 60), (1, 60))],
                      ['weeks', 'days', 'hours', 'minutes', 'seconds'])
             if num)

def timecompare(etimeun, eairfuture):
    if eairfuture == True:
        compareun = etimeun - time.time()
    if eairfuture == False:
        compareun = time.time() - etimeun
    return duration(compareun)

class Episode(object):
    def __init__(self, api_data):
        self.name = api_data['name']
        self.season = api_data['season']
        self.episode = api_data['episode']
        self.movie = api_data['is_movie']
        self.airdate = time.gmtime(api_data['air_date'])

    def strtime(self):
        return time.strftime('%A %B %d, %Y at %I:%M:%S %p',self.airdate)

    def humantime(self):
        return timecompare(self.airdate, self.isfuture())

    def isfuture(self):
        return self.airdate < time.time()

    def airing(self):
        response = ''
        if not self.movie:
            response += 'Season ' + self.season + ', Episode ' + self.episode
        response += self.name
        if self.isfuture():
            response += ' will air on '
        else:
            response += ' aired on '
        response += self.strtime() + ' GMT (' + self.humantime()
        if self.isfuture():
            response += ' from now)'
        else:
            response += ' ago)'
        return response

def episode_find(query, phenny): 
    query = query.replace('!', '')
    result = _re_full.match(query) or _re_short.match(query) or _re_movie.match(query)
    if result:
        try:
            snum = result.group('season')
        except IndexError:
            snum = 99
        enum = result.group('episode')
        uri = 'https://ponyapi.apps.xeserv.us/season/' + snum + '/episode/' + enum
        nl = query
        issearch = False
        isnextlast = False
    elif query.startswith('next'):
        uri = 'https://ponyapi.apps.xeserv.us/newest'
        nl = 'next'
        issearch = False
        isnextlast = True
    elif query.startswith('last'):
        uri = 'https://ponyapi.apps.xeserv.us/last_aired'
        nl = 'last'
        issearch = False
        isnextlast = True
    else:
        webquery = web.quote(query)
        uri = 'https://ponyapi.apps.xeserv.us/search?q=' + webquery
        nl = query
        issearch = True
        isnextlast = False
                    
    headers = [('Accept', 'application/json')]
    try:
        rec_bytes = web.get(uri, headers)
    except:
        if isnextlast is True:
            return 'nope$' + nl
        else:
            return
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    try:
        jsonstring['episodes'][0]
    except:
        try:
            jsonstring['episodes']['name']
        except:
            try:
                jsonstring['episode']['name']
            except:
                return 'nope$' + nl
    try:
        ep = Episode(jsonstring['episodes'][0])
        epnumbered = True
    except:
        try:
            ep = Episode(jsonstring['episodes'])
            epnumbered = False
        except:
            ep = Episode(jsonstring['episode'])
            epnumbered = False

    if epnumbered is True and issearch is True:
        try:
            epsecond = Episode(jsonstring['episodes'][1])
        except:
            epsecond = False
    else:
        epsecond = False

    if ep.movie:
        return ep.airing()
    elif epsecond:
        return ep.airing() + ' and ' + epsecond.airing()
    else:
        return ep.airing()

def episode(phenny, input): 
    """Finds MLP Episodes. Commands can be .ep season 2 episode 1 or .ep s2e1 or .ep return of harmony or .ep next or .ep last or .ep movie 3"""
    query = input.group(2)
    if not query: return phenny.reply('.ep what?')

    uri = episode_find(query, phenny)
    if uri: 
        if uri.startswith('nope'):
            uris = uri.split('$')
            return phenny.say("Sorry " + input.nick + ", I couldn't find the " + uris[1] + " episode.")
        else:
            phenny.say("Here's what I got, " + input.nick + ": " + uri)
            if not hasattr(phenny.bot, 'last_seen_uri'):
                phenny.bot.last_seen_uri = {}
            phenny.bot.last_seen_uri[input.sender] = uri
    else: phenny.say("Sorry " + input.nick + ", I couldn't find any episodes for '%s'." % query)
episode.commands = ['ep','episode']

if __name__ == '__main__': 
    print(__doc__.strip())
