#!/usr/bin/env python
'''
head.py - Phenny HTTP Metadata Utilities
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

Modified by Jordan Kinsley <jordan@jordantkinsley.org>
'''

import re, os.path, json, imp
import urllib.request
import urllib.parse
import urllib.error
import http.client
import http.cookiejar
import time
from datetime import timedelta
from html.entities import name2codepoint
name2codepoint['apos'] = 0x0027
import web
from tools import deprecated
import ast
import calendar
import string

cj = http.cookiejar.LWPCookieJar(os.path.join(os.path.expanduser('~/.phenny'), 'cookies.lwp'))
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

def head(phenny, input): 
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '')
    if ' ' in uri: 
        uri, header = uri.rsplit(' ', 1)
    else: uri, header = uri, None

    if not uri and hasattr(phenny, 'last_seen_uri'): 
        try: uri = phenny.last_seen_uri[input.sender]
        except KeyError: return phenny.say('?')

    if not uri.startswith('htt'): 
        uri = 'http://' + uri
    # uri = uri.replace('#!', '?_escaped_fragment_=')
    
    start = time.time()

    try:
        info = web.head(uri)
        info['status'] = '200'
    except urllib.error.HTTPError as e:
        return phenny.say(str(e.code))
    except http.client.InvalidURL:
        return phenny.say("Not a valid URI, sorry.")
    except IOError:
        return phenny.say("Can't connect to %s" % uri)

    resptime = time.time() - start

    if header is None: 
        data = []
        if 'Status' in info: 
            data.append(info['Status'])
        if 'content-type' in info: 
            data.append(info['content-type'].replace('; charset=', ', '))
        if 'last-modified' in info: 
            modified = info['last-modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if 'content-length' in info: 
            data.append(info['content-length'] + ' bytes')
        data.append('{0:1.2f} s'.format(resptime))
        phenny.reply(', '.join(data))
    else: 
        headerlower = header.lower()
        if headerlower in info: 
            phenny.say(header + ': ' + info.get(headerlower))
        else: 
            msg = 'There was no %s header in the response.' % header
            phenny.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'

r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')

@deprecated
def f_title(self, origin, match, args): 
    """.title <URI> - Return the title of URI."""
    uri = match.group(2)
    uri = (uri or '')

    if not uri and hasattr(self, 'last_seen_uri'): 
        uri = self.last_seen_uri.get(origin.sender)
    if not uri: 
        return self.msg(origin.sender, 'I need a URI to give the title of...')
    title = gettitle(uri)
    if title:
        self.msg(origin.sender, origin.nick + ': ' + title)
    else: self.msg(origin.sender, origin.nick + ': No title found')
f_title.commands = ['title']

def noteuri(phenny, input): 
    uri = input.group(1)
    if not hasattr(phenny.bot, 'last_seen_uri'): 
        phenny.bot.last_seen_uri = {}
    phenny.bot.last_seen_uri[input.sender] = uri
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'

titlecommands = r'(?:' + r'|'.join(f_title.commands) + r')'
def snarfuri(phenny, input):
    if re.match(r'(?i)' + phenny.config.prefix + titlecommands, input.group()):
        return
    uri = input.group(1)
    if input.nick in ('derpy','Chance'):
        return
    try:
        
        title = None

        youtube = re.compile('http(s)?://((www|m).)?youtube.(com|co.uk|ca)?/watch.*\?.*v\=(.*)')
        if youtube.match(uri) or re.compile('http(s)?://youtu.be/(.*)').match(uri):
            # due to changes in how Youtube gives out API access, we need a key from the config file
            if get_youtube_title(uri, phenny.config.youtube_api_key) is None:
                phenny.say("Sorry " + input.nick + " but you need to fix your URL.")
                return
            else:
                title = get_youtube_title(uri, phenny.config.youtube_api_key)

        fimfiction = re.compile('http(s)?://(www.)?fimfiction.net/story/')
        if fimfiction.match(uri):
            title = get_story_title(uri)

        if re.compile('http(s)?://(www.)?((e621)|(e926)).net/post/show/').match(uri): #e621 or e926 link
            title = ouroboros('e621',uri, phenny)
        
        if re.compile('http(s)?://(.+)?spotify.com/album/').match(uri):
            title = spotify_album(uri, phenny)
        
        if re.compile('http(s)?://(.+)?spotify.com/artist/').match(uri):
            title = spotify_artist(uri, phenny)
        
        if re.compile('http(s)?://(.+)?spotify.com/user/').match(uri):
            title = spotify_user(uri, phenny)
        
        if re.compile('http(s)?://(.+)?spotify.com/track/').match(uri):
            title = spotify_track(uri, phenny, radio=False)
        
        if re.compile('http(s)?://(.+)?ted.com/talks/').match(uri):
            title = ted(uri, phenny)
        
        if re.compile('http(s)?://(.+)?dailymotion.com/video/').match(uri):
            title = dailymotion(uri, phenny)
        
        if re.compile('http(s)?://(.+)?spotify.com/.+/track/').match(uri):
            title = spotify_track(uri, phenny, radio=True)
        
        if re.compile('http(s)?://(.+)?deviantart.com/art/').match(uri):
            title = deviantart(uri, phenny)
        
        if re.compile('http(s)?://(.+)?imgur.com/(.+)').match(uri):
            title = imgur(uri, phenny)
        
        if re.compile('http(s)?://(.+)?deviantart.com/journal/').match(uri):
            title = deviantart(uri, phenny)
        
        if re.compile('http(s)?://(.+)?soundcloud.com/').match(uri):
            title = soundcloud(uri, phenny)
        
        if re.compile('http(s)?://fav.me/').match(uri):
            title = deviantart(uri, phenny)
        
        if re.compile('http(s)?://sta.sh/').match(uri):
            title = deviantart(uri, phenny)
        
        if re.compile('http(s)?://(.+)?deviantart.com/(.+)/d').match(uri):
            title = deviantart(uri, phenny)
            
        if re.compile('http(s)?://(.+)?deviantart.com/(.+)/art/(.+)').match(uri):
            title = deviantart(uri, phenny)
        
        #if re.compile('http(s)?://(www.)?(f-list).net/c/').match(uri):
        #    title = flistchar(uri, phenny)

        if re.compile('http(s)?://(www.)?twentypercentcooler.net/post/show/').match(uri):
            title = ouroboros('twentypercentcooler',uri, phenny)

        if re.compile('http(s)?://(www.)?derpiboo((.ru)|(ru.org))(/images)?/').match(uri):
            title = derpibooru(uri, phenny)

        if re.compile('http(s)?://(www.)?derpicdn.net(/img)?/').match(uri):
            title = derpibooru(uri, phenny)

        if title:
            phenny.say(title)
        else:
            title = gettitle(uri)
            if title: phenny.msg(input.sender, '[ ' + title + ' ]')
    except http.client.HTTPException:
        return
snarfuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
snarfuri.priority = 'low'

def gettitle(uri):
    if re.compile('http(s)?://(.*).(jpg|jpeg|png|gif|tiff|bmp)').match(uri):
        return None
    if not ':' in uri: 
        uri = 'http://' + uri
    uri = uri.replace('#!', '?_escaped_fragment_=')

    title = None
    localhost = [
        'http://localhost/', 'http://localhost:80/', 
        'http://localhost:8080/', 'http://127.0.0.1/', 
        'http://127.0.0.1:80/', 'http://127.0.0.1:8080/', 
        'https://localhost/', 'https://localhost:80/', 
        'https://localhost:8080/', 'https://127.0.0.1/', 
        'https://127.0.0.1:80/', 'https://127.0.0.1:8080/', 
    ]
    for s in localhost: 
        if uri.startswith(s): 
            return

    if re.compile('http(s)?://(www.)?bad-dragon.com/').match(uri) and not check_cookie('baddragon_age_checked'):
        urllib.request.urlopen('http://bad-dragon.com/agecheck/accept')

    try: 
        redirects = 0
        while True: 
            info = web.head(uri)

            if not isinstance(info, list): 
                status = '200'
            else: 
                status = str(info[1])
                info = info[0]
            if status.startswith('3'): 
                uri = urllib.parse.urljoin(uri, info['Location'])
            else: break

            redirects += 1
            if redirects >= 25: 
                return None

        try: mtype = info['content-type']
        except: 
            return None

        try:
            # Occasionally throws type errors if a CSS file is given. 
            if not (('/html' in mtype) or ('/xhtml' in mtype)): 
                return None
        except:
            return None

        bytes = web.get(uri, isSecure=False)
        #bytes = u.read(262144)
        #u.close()

    except IOError: 
        return
    except UnicodeError:
        '''
        Due to the way Python implemented the urllib.request.urlopen() 
        function, it is not possible to correct for Unicode characters
        like € in a URL. Therefore, we just catch the error and don't
        provide a title for the link. Other options may be worth 
        exploring, and could be included here. 
        '''
        return

    m = r_title.search(bytes)
    if m: 
        title = m.group(1)
        title = title.strip()
        title = title.replace('\t', ' ')
        title = title.replace('\r', ' ')
        title = title.replace('\n', ' ')
        while '  ' in title: 
            title = title.replace('  ', ' ')
        if len(title) > 200: 
            title = title[:200] + '[...]'
        
        def e(m): 
            entity = m.group(0)
            if entity.startswith('&#x'): 
                cp = int(entity[3:-1], 16)
                return chr(cp)
            elif entity.startswith('&#'): 
                cp = int(entity[2:-1])
                return chr(cp)
            else: 
                char = name2codepoint[entity[1:-1]]
                return chr(char)
        title = r_entity.sub(e, title)

        if title: 
            title = title.replace('\n', '')
            title = title.replace('\r', '')
        else: title = None
    return title

def check_cookie(name):
    ''' checks the given name against the names of cookies in the cookie
    jar; returns true iff it finds an exact match.'''
    for cookie in cj:
        if cookie.name == name:
            return True
        else: continue
    return False

def query(vid, auth_key):
    ''' 
    returns the title, viewcount, time, and uploader of a Youtube video. 
    vid is the Youtube video ID at the end of the Youtube URL.
    '''
    
    main = 'https://www.googleapis.com/youtube/v3/videos?id='
    key = '&key=' + auth_key
    ext = '&part=snippet,contentDetails,statistics'
    
    req = web.get(main + vid + key + ext)
    data = json.loads(req, encoding='utf-8')
    try:
        data = data['items'][0]
    except IndexError: return None
    title = data['snippet']['title']
    uploader = data['snippet']['channelTitle']
    uploaded = data['snippet']['publishedAt']
    try:
        viewcount = str(data['statistics']['viewCount'])
    except (KeyError, IndexError):
        viewcount = '0'
    duration = str(data['contentDetails']['duration'])
    # a video with no likes results in IndexErrors (assuming true for ratingCount, too)
    try:
        likes = str(data['statistics']['likeCount'])
    except (KeyError, IndexError):
        likes = '0'
    try:
        dislikes = str(data['statistics']['dislikeCount'])
    except (KeyError, IndexError):
        dislikes = '0'
    
    time = iso_8601(duration)
    
    return title, viewcount, time, uploader, uploaded, likes, dislikes
    
def iso_8601(str_time):
    '''
    Google's Youtube data V3 API gives duration in an ISO 8601 format, e.g.
    P3DT4H30M44S. Each format of time, i.e. 3D, 4H, 30M, 44S are optional 
    in the string. P1D is just as valid as PT24H, for instance (and is the
    actual value returned for a video exactly 24 hours, 0 minutes, and 0 seconds long
    
    returns a string of the time, formatted like 3d 4h 30m 44s
    '''
    
    iso_8601_re = re.compile('P(?P<year>[0-9]*Y)?(?P<month>[0-9]*M)?(?P<week>[0-9]*W)?(?P<day>[0-9]*D)?(T)?(?P<hour>[0-9]*H)?(?P<minute>[0-9]*M)?(?P<second>[0-9]*S)?')
    
    found_time = re.match(iso_8601_re, str_time)
    year, month, week, day, hour, minute, second = '','','','','','',''
    return_time = ''
    if found_time.group('year'):
        year = found_time.group('year').rstrip('Y')
        return_time = return_time + year + 'y '
    if found_time.group('month'):
        month = found_time.group('month').rstrip('M')
        return_time = return_time + month + 'm '
    if found_time.group('week'):
        week = found_time.group('week').rstrip('W')
        return_time = return_time + week + 'w '
    if found_time.group('day'):
        day = found_time.group('day').rstrip('D')
        return_time = return_time + day + 'd '
    if found_time.group('hour'):
        hour = found_time.group('hour').rstrip('H')
        return_time = return_time + hour + 'h '
    if found_time.group('minute'):
        minute = found_time.group('minute').rstrip('M')
        return_time = return_time + minute + 'm '
    if found_time.group('second'):
        second = found_time.group('second').rstrip('S')
        return_time = return_time + second + 's '
    return return_time

def get_youtube_title(uri, auth_key):
    vid = None
    if 'youtu.be/' not in uri:
        if '?v=' in uri:
            vid = uri[uri.index('?v=')+3:uri.index('?v=') + 14]
        elif '&v=' in uri:
            vid = uri[uri.index('&v=')+3:uri.index('&v=') + 14]
        else:
            return None
    else:
        vid = uri[uri.rindex('be/')+3:uri.rindex('be/')+14]

    video_data = query(vid, auth_key)
    if video_data is None:
      return None
    else:
      title, views, length, uploader, uploaded, likes, dislikes = video_data
    try:
        import dateutil.parser
        isdateutil = True
        dt = dateutil.parser.parse(uploaded)
        timestamp1 = calendar.timegm(dt.timetuple())
        timestamp1 = time.gmtime(timestamp1)
        uploadedformat = time.strftime('%A %B %d, %Y at %I:%M:%S %p',timestamp1)
    except:
        isdateutil = False
    if title == '':
        return None
    percentage = get_percentage(likes, dislikes)
    if isdateutil is False:
        return "\002You\00300,04Tube\017 " + title + " - " + views + " views - Uploaded by " + uploader + " - " + length + "long - " + likes + " likes - " + dislikes + " dislikes - " + percentage + "%"
    else:
        return "\002You\00300,04Tube\017 " + title + " - " + views + " views - Uploaded by " + uploader + " on " + uploadedformat + " - " + length + "long - " + likes + " likes - " + dislikes + " dislikes - " + percentage + "%"

def get_api_story_title(uri):
    story_id = uri.split('story/')[1]
    if story_id.find('/') > 1:
        story_id = story_id.split('/')[0]
    data = web.get('https://fimfiction.net/api/story.php?story=' + story_id)
    story = json.loads(data, encoding='utf-8')['story']
    
    story_title = format_title(story['title'])
    likes = str(story['likes'])
    dislikes = str(story['dislikes'])
    percentage = get_percentage(likes, dislikes)
    author = story['author']['name'].strip('"')
    views = str(story['views'])
    words = str(story['words'])
    content_rating = int(story['content_rating'])
    chapters = str(story['chapter_count'])
    categories = ''
    updatedun = story['date_modified'] 
    updatedgmt = time.gmtime(updatedun)
    updated = time.strftime('%A %B %d, %Y at %I:%M:%S %p',updatedgmt)
    description = story['short_description']
    status = story['status']
    
    #cat_dict = story['categories']
    #for k in cat_dict:
    #    if cat_dict[k] is True:
    #        categories = categories + '[' + k + ']'
    #return story_title, likes, dislikes, percentage, author, views, words, content_rating, chapters, categories, updated, description, status
    return story_title, likes, dislikes, percentage, author, views, words, content_rating, chapters, updated, description, status
    
def format_title(title):
    title = title.strip('"')
    title = title.replace('&#039;','\'')
    title = title.replace('&amp;','&')
    title = title.replace('&quot;','"')
    title = title.replace('&lt;','<')
    title = title.replace('&gt;','>')
    return title
    
def get_percentage(likes, dislikes):
    percentage = ''
    if int(likes) > 0 or int(dislikes) > 0:
        percentage = (float(likes) / (float(dislikes) + float(likes))) * 100
        percentage = str(round(percentage, 2))
    else:
        # no likes and dislikes
        percentage = '0.00'
    return percentage

def smart_truncate(content, phenny):
    if phenny.config.tag_list_length:
        try:
            length=int(phenny.config.tag_list_length)
        except:
            return("The tag_list_length option is not set correctly, please fix it",0)
        if len(content) <= length:
            return(content, 0)
        else:
            tag_list = content[:length]
            unlisted_tags = len(content) - len(tag_list)
            return(tag_list, unlisted_tags)
    else:
        return("Please set the tag_list_length option in the config",0)


def ouroboros(site, uri, phenny):
    # e621 and twentypercentcooler use the same software
    # TODO: load tag file; compare tags, generate title
    #load a list of unimportant tags from a file. possible regex?
    title = ''
    def get_id(link):
        exp = '(.*)show/(?P<id>[0-9]*)/?'
        return re.search(exp, link).group('id')
    post_id = get_id(uri)
    json_data = web.get('https://{0}.net/post/show.json?id={1}'.format(site, post_id))
    postdata = json.loads(json_data, encoding='utf-8')
    tags = postdata['tags'].split(' ')

    ratings = { 's' : 'Safe', 'q' : 'Questionable', 'e' : 'Explicit' }
    if postdata['rating'] in ratings:
        rating = ratings[postdata['rating']]
    else:
        rating = 'Unknown'
    rating_list = rating.split(' ')
    if site == 'e621':
        artists = postdata['artist']
        tags = [tag for tag in tags if tag not in artists]
    else:
        artists = ['none']
    isdateutil = True
    created_unix = postdata['created_at']['s']
    uploader = postdata['author']
    width = postdata['width']
    height = postdata['height']
    if site == 'e621':
        title_starter = '\002e621 -- '
    else:
        title_starter = '\00220% Cooler -- '
    info = {'site':site, 'title_starter':title_starter, 'tags':tags, 'ratings':rating_list, 'artists':artists, 'created_unix':created_unix, 'isdateutil':isdateutil, 'uploader':uploader, 'width':width, 'height':height, 'upvotes':0, 'downvotes':0, 'mime':None}
    title = tags_parser(info, phenny)
        
    
    return title

def tags_parser(info, phenny):
    site = info['site']
    tags = info['tags']
    ratings = info['ratings']
    artists = info['artists']
    created_unix = info['created_unix']
    isdateutil = info['isdateutil']
    uploader = info['uploader']
    width = info['width']
    height = info['height']
    upvotes = info['upvotes']
    downvotes = info['downvotes']
    mime = info['mime']
    (truncated, num_truncated) = smart_truncate(tags, phenny)
    tag_string = (", ".join(truncated))
    if num_truncated > 0:
        tag_string = (tag_string + " (" + str(num_truncated) + " more)")
    num_artists = len(artists)
    num_ratings = len(ratings)
    if isdateutil is True:
        timestamp1 = time.gmtime(created_unix)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
    if num_artists == 2:
        artists_combiner = " and "
    else:
        artists_combiner = ", "
    if site == 'derpibooru':
        artists = [artist[7:] for artist in artists]
    if num_artists < 1:
        artists = ['unknown']
    artists_string = (artists_combiner.join(artists))
    ratings_string = (", ".join(ratings))
    title = info['title_starter']
    if num_ratings > 1:
        ratings_tense = 'Ratings:\017 '
    else:
        ratings_tense = 'Rating:\017 '
    title = title + ratings_tense + ratings_string
    if site != 'twentypercentcooler':
        if num_artists > 1:
            artists_tense = '\002 Artists:\017 '
        else:
            artists_tense = '\002 Artist:\017 '
        title = title + artists_tense + artists_string
    title = title + ' \002Tags:\017 ' + tag_string + '\002 Uploaded by:\017 ' + uploader
    if site == 'derpibooru':
        title = title + ' \002↑' + str(upvotes) + '/' + str(downvotes) + '↓\017'
    if isdateutil is True:
        title = title + ' \002Uploaded on\017 ' + created_format
    title = title + ' \002Resolution:\017 ' + str(width) + '×' + str(height)
    if site == 'derpibooru':
        title = title + ' \002Type:\017 ' + mime
    return title

def derpibooru(uri, phenny):
    # TODO: research derpibooru's API and get data
    def get_id(link):
        exp = 'https?://.*/(?P<id>[0-9]+)'
        return re.search(exp, link).group('id')
    id = get_id(uri)
    if not id:
        return gettitle(uri)
    json_data = web.get('https://derpibooru.org/{0}.json'.format(id))
    postdata = json.loads(json_data, encoding='utf-8')
    if 'deletion_reason' in postdata:
        deleted = postdata['deletion_reason']
        created_zulu = postdata['created_at']
        try:
            import dateutil.parser
            dt = dateutil.parser.parse(created_zulu)
            created_unix = calendar.timegm(dt.timetuple())
            timestamp1 = time.gmtime(created_unix)
            created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
            created_format = ", it was uploaded on " + created_format
        except:
            created_format = ""
        
        return '\002Derpibooru -- \017This image was deleted because of "' + deleted + '"' + created_format
    tags = postdata['tags'].split(', ')
    
    artists = []
    for tag in tags:
        if tag.startswith('artist:'):
            artists.append(tag)
    # ratings are tags on Derpibooru
    ratings = []
    for tag in tags:
        if tag in {'explicit', 'grimdark', 'grotesque', 'questionable', 'safe', 'semi-grimdark', 'suggestive'}:
            ratings.append(tag)
    if not ratings:
        ratings = ['unknown']
    tags = [tag for tag in tags if tag not in artists]
    tags = [tag for tag in tags if tag not in ratings]
    
    created_zulu = postdata['created_at']
    uploader = postdata['uploader']
    upvotes = postdata['upvotes']
    downvotes = postdata['downvotes']
    width = postdata['width']
    height = postdata['height']
    mime = postdata['mime_type']
    site = 'derpibooru'
    title_starter = '\002Derpibooru -- '
    try:
        import dateutil.parser
        isdateutil = True
        dt = dateutil.parser.parse(created_zulu)
        created_unix = calendar.timegm(dt.timetuple())
    except:
        isdateutil = False
        created_unix = 0
    
    info = {'site':site, 'title_starter':title_starter, 'tags':tags, 'ratings':ratings, 'artists':artists, 'created_unix':created_unix, 'isdateutil':isdateutil, 'uploader':uploader, 'width':width, 'height':height, 'upvotes':upvotes, 'downvotes':downvotes, 'mime':mime}
    title = tags_parser(info,phenny)
        
    return title

def get_story_title(uri):
    #story_title, likes, dislikes, percentage, author, views, words, content_rating, chapters, categories, updated, description, status = get_api_story_title(uri)
    story_title, likes, dislikes, percentage, author, views, words, content_rating, chapters, updated, description, status = get_api_story_title(uri)
    title = '\002\00312,00FIMFiction\017 '
    if content_rating > 1:
        title = title + '\u0002!!*NSFW*!!\u000F - '
    title = title + story_title + " by " + author
    if chapters:
        title = title + ' - ' + str(chapters)
        if int(chapters) > 1:
            title = title + ' chapters'
        else:
            title = title + ' chapter'
    #title = title + " - " + views + " views - " + categories + ' -- ' + status + ' -- ' + words + ' words'
    title = title + " - " + views + " views" + ' -- ' + status + ' -- ' + words + ' words'
    title = title + " - Likes: " + likes + " - Dislikes: " + dislikes + " - " + percentage + "% - last updated on " + updated + " - " + description
    return title

def flistchar(uri, phenny):
    if hasattr(phenny.config, 'f_list_account') and hasattr(phenny.config, 'f_list_password') :
        ticketuri = 'https://www.f-list.net/json/getApiTicket.php'
        ticketquery = {'account' : phenny.config.f_list_account, 'password' : phenny.config.f_list_password}
        ticketjson = web.post(ticketuri, ticketquery)
        
        ticketstr = str(ticketjson)
        ticketdict = ast.literal_eval(ticketstr)
        ticket = ticketdict['ticket']
        
        urilist = uri.split('/')
        urlcharname = urilist[4]
        urlcharname = web.unquote(urlcharname)
        charuri = 'https://www.f-list.net/json/api/character-get.php'
        charquery = {'name' : urlcharname}
        charjson = web.post(charuri, charquery)
        
        charstr = str(charjson)
        chardict = ast.literal_eval(charstr)
        try:
            charname = chardict['character']['name']
        except:
            errname = chardict['error']
        
        try:
            titlestr = 'Error - ' + errname
        except UnboundLocalError:
            titlestr = '\002\00312,01F-List\017 - ' + charname
        
        
        return titlestr
    else:
        return
def deviantart(uri, phenny):
    apiuri = 'http://backend.deviantart.com/oembed?url=' + web.quote(uri)
    try:
        rec_bytes = web.get(apiuri, isSecure=False)
    except:
        return
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    type = jsonstring['type']
    title = jsonstring['title']
    category = jsonstring['category']
    author = jsonstring['author_name']
    safe = jsonstring['safety']
    uploaded = jsonstring['pubdate']
    views = str(jsonstring['community']['statistics']['_attributes']['views'])
    favs = str(jsonstring['community']['statistics']['_attributes']['favorites'])
    try:
        import dateutil.parser
        isdateutil = True
        dt = dateutil.parser.parse(uploaded)
        timestamp1 = calendar.timegm(dt.timetuple())
        timestamp1 = time.gmtime(timestamp1)
        uploadedformat = time.strftime('%A %B %d, %Y at %I:%M:%S %p',timestamp1)
    except:
        isdateutil = False
    if re.compile('nonadult').match(safe):
        nsfw = False
    else:
        nsfw = True
    if nsfw is True:
        if isdateutil is True:
            return '\002!!NSFW!! \00300,03DeviantArt\017 ' + title + ' by ' + author + ' - ' + category + ' - ' + type + ' uploaded on ' + uploadedformat + ' - ' + views + ' views - ' + favs + ' favs'
        else:
            return '\002!!NSFW!! \00300,03DeviantArt\017 ' + title + ' by ' + author + ' - ' + category + ' - ' + type + ' - ' + views + ' views - ' + favs + ' favs'
    else:
        if isdateutil is True:
            return '\002\00300,03DeviantArt\017 ' + title + ' by ' + author + ' - ' + category + ' - ' + type + ' uploaded on ' + uploadedformat + ' - ' + views + ' views - ' + favs + ' favs'
        else:
            return '\002\00300,03DeviantArt\017 ' + title + ' by ' + author + ' - ' + category + ' - ' + type + ' - ' + views + ' views - ' + favs + ' favs'
    
def spotify_album(uri, phenny):
    idsplit = uri.split('/')
    id = idsplit[4]
    apiuri = 'https://api.spotify.com/v1/albums/' + id
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    jsonstring = json.loads(rec_bytes)
    album = jsonstring['name']
    artistarray = jsonstring['artists']
    if len(artistarray) > 1:
        multipleartists = True
    else:
        multipleartists = False
    if multipleartists is False:
        artist = artistarray[0]['name']
    else:
        artist = "Various Artists"
    released = jsonstring['release_date']
    try:
        import dateutil.parser
        isdateutil = True
        dt = dateutil.parser.parse(released)
        timestamp1 = calendar.timegm(dt.timetuple())
        timestamp1 = time.gmtime(timestamp1)
        if re.compile('day').match(jsonstring['release_date_precision']):
            releasedformat = time.strftime('on %A %B %d, %Y',timestamp1)
        else:
            if re.compile('month').match(jsonstring['release_date_precision']):
                releasedformat = time.strftime('in %B, %Y',timestamp1)
            else:
                if re.compile('year').match(jsonstring['release_date_precision']):
                   releasedformat = time.strftime('in %Y',timestamp1)
                else:
                    isdateutil = False
    except:
        isdateutil = False
    type = jsonstring['album_type']
    type = string.capwords(type)
    if isdateutil is True:
        return '\002\00303,01Spotify\017 ' + type + ' - ' + artist + ' - ' + album + ' released ' + releasedformat
    else:
        return '\002\00303,01Spotify\017 ' + type + ' - ' + artist + ' - ' + album

def spotify_artist(uri, phenny):
    idsplit = uri.split('/')
    id = idsplit[4]
    apiuri = 'https://api.spotify.com/v1/artists/' + id
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    jsonstring = json.loads(rec_bytes)
    followers = str(jsonstring['followers']['total'])
    name = jsonstring['name']
    return '\002\00303,01Spotify\017 ' + name + ' - ' + followers + ' followers'
    
def spotify_user(uri, phenny):
    idsplit = uri.split('/')
    id = idsplit[4]
    apiuri = 'https://api.spotify.com/v1/users/' + id
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    jsonstring = json.loads(rec_bytes)
    if jsonstring["display_name"]:
        name = jsonstring["display_name"]
    else:
        name = jsonstring["id"]
    followers = str(jsonstring["followers"]["total"])
    return '\002\00303,01Spotify\017 ' + name + ' - ' + followers + ' followers'

def spotify_track(uri, phenny, radio):
    idsplit = uri.split('/')
    if radio is False:
        id = idsplit[4]
    else:
        id = idsplit[5]
    apiuri = 'https://api.spotify.com/v1/tracks/' + id
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    jsonstring = json.loads(rec_bytes)
    track = jsonstring['name']
    album = jsonstring['album']['name']
    artistarray = jsonstring['artists']
    if len(artistarray) > 1:
        multipleartists = True
    else:
        multipleartists = False
    if multipleartists is False:
        artist = artistarray[0]['name']
    else:
        artist = "Various Artists"
    albumid = jsonstring['album']['id']
    albumurl = 'https://api.spotify.com/v1/albums/' + albumid
    try:
        rec_bytes_album = web.get(albumurl)
        jsonstringalbum = json.loads(rec_bytes_album)
        released = jsonstringalbum['release_date']
    except:
        isdateutil = False
    try:
        import dateutil.parser
        isdateutil = True
        dt = dateutil.parser.parse(released)
        timestamp1 = calendar.timegm(dt.timetuple())
        timestamp1 = time.gmtime(timestamp1)
        if re.compile('day').match(jsonstringalbum['release_date_precision']):
            releasedformat = time.strftime('on %A %B %d, %Y',timestamp1)
        else:
            if re.compile('month').match(jsonstringalbum['release_date_precision']):
                releasedformat = time.strftime('in %B, %Y',timestamp1)
            else:
                if re.compile('year').match(jsonstringalbum['release_date_precision']):
                   releasedformat = time.strftime('in %Y',timestamp1)
                else:
                    isdateutil = False
    except:
        isdateutil = False
    milliseconds = jsonstring['duration_ms']
    seconds=(milliseconds/1000)%60
    minutes=(milliseconds/(1000*60))%60
    minutes = str(int(minutes))
    seconds = str(round(seconds)).zfill(2)
    tracktime = minutes + ":" + seconds
    if isdateutil is True:
        return '\002\00303,01Spotify\017 ' + track + ' - ' + artist + ' - ' + album + ' - ' + tracktime + ' released ' + releasedformat
    else:
        return '\002\00303,01Spotify\017 ' + track + ' - ' + artist + ' - ' + album + ' - ' + tracktime
    
def smart_truncate_soundcloud(content):
    suffix='...'
    length=int(150)
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix

def soundcloud(uri, phenny):
    apiuri = "https://soundcloud.com/oembed?format=json&url=" + uri
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    provider = jsonstring['provider_name']
    title = jsonstring['title']
    description = jsonstring['description']
    if description is None:
        descriptiont = False
    else:
        descriptiont = True
        description = smart_truncate_soundcloud(description)
    if descriptiont is True:
        return '\002\00307,14' + provider + '\017 ' + title + ' - ' + description
    else:
        return '\002\00307,14' + provider + '\017 ' + title
    
def ted(uri, phenny):
    apiuri = "https://www.ted.com/services/v1/oembed.json?url=" + uri
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    title = jsonstring['title']
    description = jsonstring['description']
    description = smart_truncate_soundcloud(description)
    return '\002\00304,00TED Talks\017 ' + title + ' - ' + description

def dailymotion(uri, phenny):
    apiuri = 'https://www.dailymotion.com/services/oembed?format=json&url=' + uri
    try:
        rec_bytes = web.get(apiuri)
    except:
        return
    try:
        jsonstring = json.loads(rec_bytes)
    except:
        return
    title = jsonstring['title']
    uploader = jsonstring['author_name']
    provider = jsonstring['provider_name']
    return '\002\00300,02' + provider + '\017 ' + title + ' by ' + uploader
    
def imgur(uri, phenny):
    if hasattr(phenny.config, 'imgur_client_id'):
        client_id = phenny.config.imgur_client_id
    else:
        return
    apis = Imgurfunctions(client_id)
    startinclass = False
    m = re.compile('http(s)?://(.+)?imgur.com/((?P<itype>a|gallery(/a)?|r/(?P<reddit>.+))/)?(?P<iid>[^\./]+)(?P<extension>\.[a-z]{3})?(/comment/(?P<comment_id>\d+)$)?').match(uri)
    print(m)
    if m.group('comment_id'):
        return apis.comments(m)
    elif m.group('itype') == 'gallery':
        return apis.gallery(m, startinclass, 0)
    elif m.group('itype') == 'gallery/a':
        return apis.galleryalbum(m, startinclass, 0)
    elif m.group('itype') == 'a':
        return apis.album(m, startinclass, 0)
    elif not m.group('itype'):
        return apis.image(m, startinclass, 0)
    elif m.group('itype').startswith('r/'):
        return apis.reddit(m, startinclass, 0)

class Imgurfunctions:
    def __init__(self, client_id):
        self.headers = [('Authorization', 'Client-ID ' + client_id)]
        self.imgurcolors = '\002\00309,01Imgur\017 '
    def comments(self, m):
        cid = m.group('comment_id')
        rec_bytes = web.get('https://api.imgur.com/3/comment/'+cid, self.headers)
        jsonstring = json.loads(rec_bytes)
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        comment = jsonstring['data']['comment']
        author = jsonstring['data']['author']
        return self.imgurcolors + '\002Comment\017 - ' + comment + ' - by ' + author + ' on ' + created_format
    def gallery(self, m, startinclass, origin):
        if origin == 1:
            return
        iid = m.group('iid')
        
        try:
            rec_bytes = web.get('https://api.imgur.com/3/gallery/image/'+iid, self.headers)
        except:
            if startinclass == False:
                return self.galleryalbum(m, True, 1)
            else:
                return self.galleryalbum(m, True, origin)
        jsonstring = json.loads(rec_bytes)
        title = jsonstring['data']['title']
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        mime = jsonstring['data']['type']
        ups = jsonstring['data']['ups']
        downs = jsonstring['data']['downs']
        animated = jsonstring['data']['animated']
        width = jsonstring['data']['width']
        height = jsonstring['data']['height']
        author = jsonstring['data']['account_url']
        reply = self.imgurcolors
        if title:
            reply += title + ' -'
        else:
            reply += 'No Title -'
        if author:
            reply += ' by ' + author
        else:
            reply += ' by Anonymous'
        reply += ' \002↑' + str(ups) + '/' + str(downs) + '↓\017 Uploaded on ' + created_format + ' \002Resolution:\017' + str(width) + '×' + str(height) + ' \002Type:\017' + mime
        if animated == True:
            reply += ' Animated'
        return reply
    def galleryalbum(self, m, startinclass, origin):
        if origin == 2:
            return
        iid = m.group('iid')
        try:
            rec_bytes = web.get('https://api.imgur.com/3/gallery/album/'+iid, self.headers)
        except:
            if startinclass == False:
                return self.album(m, True, 2)
            else:
                return self.album(m, True, origin)
        jsonstring = json.loads(rec_bytes)
        title = jsonstring['data']['title']
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        author = jsonstring['data']['account_url']
        ups = jsonstring['data']['ups']
        downs = jsonstring['data']['downs']
        reply = self.imgurcolors + 'Album - '
        if title:
            reply += title + ' -'
        else:
            reply += 'No Title -'
        if author:
            reply += ' by ' + author
        else:
            reply += ' by Anonymous'
        reply += ' \002↑' + str(ups) + '/' + str(downs) + '↓\017 Uploaded on ' + created_format
        return reply 
    def album(self, m, startinclass, origin):
        if origin == 3:
            return
        iid = m.group('iid')
        try:
            rec_bytes = web.get('https://api.imgur.com/3/album/'+iid, self.headers)
        except:
            if startinclass == False:
                return self.image(m, True, 3)
            else:
                return self.image(m, True, origin)
        jsonstring = json.loads(rec_bytes)
        title = jsonstring['data']['title']
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        author = jsonstring['data']['account_url']
        reply = self.imgurcolors + 'Album - '
        if title:
            reply += title + ' -'
        else:
            reply += 'No Title -'
        if author:
            reply += ' by ' + author
        else:
            reply += ' by Anonymous'
        reply += ' Uploaded on ' + created_format
        return reply
    def image(self, m, startinclass, origin):
        if origin == 4:
            return
        iid = m.group('iid')
        try:
            rec_bytes = web.get('https://api.imgur.com/3/image/'+iid, self.headers)
        except:
            if startinclass == False:
                return self.gallery(m, True, 4)
            else:
                return self.gallery(m, True, origin)
        jsonstring = json.loads(rec_bytes)
        title = jsonstring['data']['title']
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        mime = jsonstring['data']['type']
        animated = jsonstring['data']['animated']
        width = jsonstring['data']['width']
        height = jsonstring['data']['height']
        reply = self.imgurcolors
        if title:
            reply += title + ' -'
        else:
            reply += 'No Title -'
        reply += ' Uploaded on ' + created_format + ' \002Resolution:\017' + str(width) + '×' + str(height) + ' \002Type:\017' + mime
        if animated == True:
            reply += ' Animated'
        return reply
    def reddit(self, m, startinclass, origin):
        iid = m.group('iid')
        subreddit = m.group('reddit')
        try:
            rec_bytes = web.get('https://api.imgur.com/3/gallery/r/' + subreddit + '/' + iid, self.headers)
        except:
            return
        jsonstring = json.loads(rec_bytes)
        title = jsonstring['data']['title']
        timestamp = jsonstring['data']['datetime']
        timestamp1 = time.gmtime(timestamp)
        created_format = time.strftime('%A %B %d, %Y at %I:%M:%S %p GMT',timestamp1)
        mime = jsonstring['data']['type']
        animated = jsonstring['data']['animated']
        width = jsonstring['data']['width']
        height = jsonstring['data']['height']
        subreddit = jsonstring['data']['section']
        reply = self.imgurcolors
        if title:
            reply += title + ' -'
        else:
            reply += 'No Title -'
        reply += ' Uploaded to /r/' + subreddit + ' on ' + created_format + ' \002Resolution:\017' + str(width) + '×' + str(height) + ' \002Type:\017' + mime
        if animated == True:
            reply += ' Animated'
        return reply
        

if __name__ == '__main__': 
    print(__doc__.strip())
