#!/usr/bin/python3
'''
rule34.py - rule 34 module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>

e621 and twentypercentcooler modifications by Jordan Kinsley <jordan@jordantkinsley.org>
'''

from urllib.parse import quote as urlquote
from urllib.parse import quote_plus as urlquoteplus
from urllib.error import HTTPError
from tools import GrumbleError
import web
import lxml.html

def rule34(phenny, input):
    """.rule34 <query> - Rule 34: If it exists there is porn of it."""

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
    # we're going to assume users know what to search for. :S
    try:
        req = web.get("http://e621.net/post?tags={0}".format(urlquoteplus(q)))
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")
    
    doc = lxml.html.fromstring(req)
    doc.make_links_absolute('http://e621.net/')
    thumbs = doc.find_class('thumb')
    if len(thumbs) <= 0:
        phenny.reply("Huh. e621 is missing {0}".format(q))
        return
    
    try:
        link = thumbs[0].find('a').attrib['href']
    except AttributeError:
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")
    # TODO: check Rating:<> tag to see if the link is really NSFW
    # For now, keep this because we have no idea, and it's better to ere on the side of caution
    response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
    phenny.reply(response)
e621.rule = (['e621'], r'(.*)')

def tpc(phenny, input):
    '''.tpc <query> - returns the image for any query from twentypercentcooler.net 
    (all links tagged as NSFW)Query must be formatted like a normal e621 search: all 
    tags have their spaces replaced with underscores.'''
    q = input.group(2)
    if not q:
        phenny.say(tpc.__doc__.strip())
        return
    # we're going to assume users know what to search for. :S
    try:
        req = web.get("http://twentypercentcooler.net/post?tags={0}".format(urlquoteplus(q)))
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")
    
    doc = lxml.html.fromstring(req)
    doc.make_links_absolute('http://twentypercentcooler.net/')
    thumbs = doc.find_class('thumb')
    if len(thumbs) <= 0:
        phenny.reply("Huh. Twenty Percent Cooler is missing {0}".format(q))
        return
    
    try:
        link = thumbs[0].find('a').attrib['href']
    except AttributeError:
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")
    # TODO: check Rating:<> tag to see if the link is really NSFW
    # For now, keep this because we have no idea, and it's better to ere on the side of caution
    response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
    phenny.reply(response)
    
tpc.rule = (['tpc','twentypercentcooler','ponies'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
