#!/usr/bin/python3
'''
rule34.py - rule 34 module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>

e621 and twentypercentcooler modifications by Jordan Kinsley <jordan@jordantkinsley.org>
'''

# TODO: extract duplicate and make it into a seperate function. 
# code duplication is killing this module.

from urllib.parse import quote as urlquote
from urllib.parse import quote_plus as urlquoteplus
from urllib.error import HTTPError
from tools import GrumbleError
import web
import json
import lxml.html

def rule34(phenny, input):
    """.rule34 <query> - Rule 34: If it exists there is porn of it."""
    
    if check_nsfw(phenny, input):
        return
    q = input.group(2)
    if not q:
        phenny.say(rule34.__doc__.strip())
        return

    try:
        req = web.get("http://rule34.xxx/index.php?page=post&s=list&tags={0}".format(urlquote(q)))
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    doc = lxml.html.fromstring(req)
    doc.make_links_absolute('http://rule34.xxx/')
    thumbs = doc.find_class('thumb')
    if len(thumbs) <= 0:
        phenny.reply("You just broke Rule 34! Better start uploading...")
        return

    try:
        link = thumbs[0].find('a').attrib['href']
    except AttributeError:
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
    phenny.reply(response)
rule34.rule = (['rule34'], r'(.*)')

def e621(phenny, input):
    '''.e621 <query> - returns the first image for any query from e621.net (all links tagged as NSFW). 
    Query must be formatted like a normal e621 search: all tags have their spaces replaced with 
    underscores.'''
    
    q = input.group(2)
    if not q:
        phenny.say(e621.__doc__.strip())
        return
    sfw = False
    if check_nsfw(phenny, input):
        if q.lower() in ('rating:explicit','rating:questionable','rating:e','rating:q'):
            q = q.replace('rating:explicit','rating:safe')
            q = q.replace('rating:questionable','rating:safe')
            q = q.replace('rating:e','rating:s')
            q = q.replace('rating:q','rating:s')
        else: q = q + ' rating:safe'
        sfw = True
    # we're going to assume users know what to search for. :S
    try:
        #the json api is super efficient compared to loading a whole page.
        #having less data to parse makes everything else faster
        req = web.get("http://e621.net/post/index.json?tags={0}".format(urlquoteplus(q)))
    except (HTTPError, IOError):
        phenny.say('Oopsies, looks like the Internet is broken.')
    
    results = json.loads(req, encoding='utf-8')

    if len(results) <= 0:
        phenny.reply("Huh. e621 is missing {0}".format(q))
        return
    
    try:
        link = 'http://e621.net/post/show/{0}/'.format(results[0]['id'])
    except AttributeError:
        phenny.say('Oopsies, looks like the Internet is broken.')

    tags = results[0]
    rating = tags['rating']
    if rating in ('q','e'):
        response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
        phenny.reply(response)
    else:
        if sfw:
            link = link.replace('621','926')
        phenny.reply(link)
e621.rule = (['e621'], r'(.*)')

def tpc(phenny, input):
    '''.tpc <query> - returns the image for any query from twentypercentcooler.net 
    (all links tagged as NSFW)Query must be formatted like a normal twentypercentcooler search: all 
    tags have their spaces replaced with underscores.'''
    
    q = input.group(2)
    
    if not q:
        phenny.say(tpc.__doc__.strip())
        return
    sfw = False
    if check_nsfw(phenny, input):
        if q.lower() in ('rating:explicit','rating:questionable','rating:e','rating:q'):
            q.replace('rating:explicit','rating:safe')
            q.replace('rating:questionable','rating:safe')
            q.replace('rating:e','rating:s')
            q.replace('rating:q','rating:s')
        else: q.append('rating:safe')
        sfw = True
    # we're going to assume users know what to search for. :S
    try:
        req = web.get("http://twentypercentcooler.net/post/index.json?tags={0}".format(urlquoteplus(q)))
    except (HTTPError, IOError):
        phenny.say('Oopsies, looks like the Internet is broken.')
    
    results = json.loads(req, encoding='utf-8')

    if len(results) <= 0:
        phenny.reply("Huh. twentypercentcooler is missing {0}".format(q))
        return
    
    try:
        link = 'http://twentypercentcooler.net/post/show/{0}/'.format(results[0]['id'])
    except AttributeError:
        phenny.say('Oopsies, looks like the Internet is broken.')

    tags = results[0]
    rating = tags['rating']
    if rating in ('q','e'):
        response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
        phenny.reply(response)
    else:
        phenny.reply(link)
tpc.rule = (['tpc','twentypercentcooler','ponies'], r'(.*)')

def check_nsfw(phenny, input):
    if input.sender not in phenny.config.nsfw:
        q = input.group(2) # we can assume q has a value because we wouldn't call this function if it didn't
        if q.lower() in ('rating:explicit','rating:questionable','rating:e','rating:q'):
            # if someone is legit trying to break the rules by searching for an explicit image
            phenny.msg('MemoServ', 'SEND {0} {2} in {1} tried to break the rules!'.format(phenny.config.owner, input.sender, input.nick))
        return True
    else: return False

if __name__ == '__main__':
    print(__doc__.strip())
