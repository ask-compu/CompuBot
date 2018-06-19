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

def episode_find(query, phenny): 
    query = query.replace('!', '')
    if _re_full.match(query):
        regex = _re_full
        results = regex.findall(query)
        snum = results[0].group('season')
        enum = results[0].group('episode')
        uri = 'https://ponyapi.apps.xeserv.us/season/' + snum + '/episode/' + enum
        nl = query
        issearch = False
        isnextlast = False
    elif _re_short.match(query):
        regex = _re_short
        results = regex.findall(query)
        snum = results[0].group('season')
        enum = results[0].group('episode')
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
    elif _re_movie.match(query):
        regex = _re_movie
        results = regex.findall(query)
        mnum = results[0].group('episode')
        uri = 'https://ponyapi.apps.xeserv.us/season/99/episode/' + mnum
        nl = query
        issearch = False
        isnextlast = False
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
        epname = jsonstring['episodes'][0]['name']
        eps = str(jsonstring['episodes'][0]['season'])
        epe = str(jsonstring['episodes'][0]['episode'])
        etimeun = jsonstring['episodes'][0]['air_date']
        movie = jsonstring['episodes'][0]['is_movie']
        epnumbered = True
    except:
        try:
            epname = jsonstring['episodes']['name']
            eps = str(jsonstring['episodes']['season'])
            epe = str(jsonstring['episodes']['episode'])
            etimeun = jsonstring['episodes']['air_date']
            movie = jsonstring['episodes']['is_movie']
            epnumbered = False
        except:
            epname = jsonstring['episode']['name']
            eps = str(jsonstring['episode']['season'])
            epe = str(jsonstring['episode']['episode'])
            etimeun = jsonstring['episode']['air_date']
            movie = jsonstring['episode']['is_movie']
            epnumbered = False
    etimegmt = time.gmtime(etimeun)
    etimeus = time.strftime('%A %B %d, %Y at %I:%M:%S %p',etimegmt)
    if epnumbered is True and issearch is True:
        try:
            epname2 = jsonstring['episodes'][1]['name']
            eps2 = str(jsonstring['episodes'][1]['season'])
            epe2 = str(jsonstring['episodes'][1]['episode'])
            etimeun2 = jsonstring['episodes'][1]['air_date']
            movie2 = jsonstring['episodes'][1]['is_movie']
            epsecond = True
            etimegmt2 = time.gmtime(etimeun2)
            etimeus2 = time.strftime('%A %B %d, %Y at %I:%M:%S %p',etimegmt2)
        except:
            epsecond = False
    else:
        epsecond = False
    if epsecond is True:
        if movie is True:
            if etimeun < time.time():
                euntil = timecompare(etimeun, False)
                return epname + ' aired on ' + etimeus + ' GMT (' + etimeun + ' ago)'
            elif etimeun > time.time():
                euntil = timecompare(etimeun, True)
                return epname + ' will air on ' + etimeus + ' GMT (' + etimeun + ' from now)'
        else:
            if etimeun < time.time():
                euntil = timecompare(etimeun, False)
                response = 'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' aired on ' + etimeus + ' GMT (' + euntil + ' ago) and Season ' + eps2 + ', '
                if etimeun2 > time.time():
                    euntil2 = timecompare(etimeun2, True)
                    response = response + 'Episode ' + epe2 + ', ' + epname2 + ' will air on ' + etimeus2 + ' GMT (' + euntil2 + ' from now)'
                elif etimeun2 < time.time():
                    euntil2 = timecompare(etimeun2, False)
                    response = response + 'Episode ' + epe2 + ', ' + epname2 + ' aired on ' + etimeus2 + ' GMT (' + euntil2 + ' ago)'
                return response
            elif etimeun > time.time():
                euntil = timecompare(etimeun, True)
                response =  'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' will air on ' + etimeus + ' GMT (' + etimeun + ' from now) and Season ' + eps2 + ', '
                if etimeun2 > time.time():
                    euntil2 = timecompare(etimeun2, True)
                    response = response + 'Episode ' + epe2 + ', ' + epname2 + ' will air on ' + etimeus2 + ' GMT (' + euntil2 + ' from now)'
                elif etimun2 < time.time():
                    euntil2 = timecompare(etimeun2, False)
                    response = response + 'Episode ' + epe2 + ', ' + epname2 + ' aired on ' + etimeus2 + ' GMT (' + euntil2 + ' ago)'
                return response
                    
                    
    else:
        if movie is True:
            if etimeun < time.time():
                euntil = timecompare(etimeun, False)
                return epname + ' aired on ' + etimeus + ' GMT (' + etimeun + ' ago)'
            elif etimeun > time.time():
                euntil = timecompare(etimeun, True)
                return epname + ' will air on ' + etimeus + ' GMT (' + etimeun + ' from now)'
        else:
            if etimeun < time.time():
                euntil = timecompare(etimeun, False)
                return 'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' aired on ' + etimeus + ' GMT (' + euntil + ' ago)'
            elif etimeun > time.time():
                euntil = timecompare(etimeun, True)
                return 'Season ' + eps + ', Episode ' + epe + ', ' + epname + ' will air on ' + etimeus + ' GMT (' + euntil + ' from now)'
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
    
    
    

if __name__ == '__main__': 
    print(__doc__.strip())
