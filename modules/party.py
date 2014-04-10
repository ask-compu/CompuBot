#!/usr/bin/python3
'''
party.py - Pinkie's new nick greeting module
(C) 2012 Jordan Kinsley <jordan@jordantkinsley.org>
(C) 2013 Kazune <kazunekit@gmail.com>
GPLv2 or later

This module checks for when a new nick joins the channel, and if the nick 
hasn't been seen before, she will throw them a party. 
'''

import os, sqlite3, re

#These ponies get Pinkie's VIP party. :3c
vip = ('Kinsley','Cocoa','MalevolentSpoon','TiredFoal','Aurora','Lapsus','Thorinair','Izia','Shutter')
ignore = ['Pony_\d']

class PartyGoer():
    __ignore = ignore
    def __conn_init(self):
        try:
            cursor = self.conn.cursor()
        except:
            self.__caller = os.urandom(16)
            self.conn = sqlite3.connect(self.db)
            return self.__caller

    def __conn_des(self, caller):
        try:
            self.conn.commit()
        except sqlite3.ProgrammingError:
            pass
        finally:
            if self.__caller == caller:
                self.conn.close()

    def __check_dirty(self):
        intersect = self.current.intersection(self.old)
        return set(o for o in intersect if self.old[o] != self.current[o])

    def __str__(self):
        return self.nick
    def __init__(self, phenny, nick, user, host):
        if re.compile('('+')|('.join(self.__ignore)+')').match(nick):
            return None
        self.db = phenny.party_db
        self.nick = nick
        hash = self.__conn_init()
        self.data = {
                'nick': None,
                'nickid' : None,
                'channelid' : None,
                'channel' : None,
                'hostid' : None,
                'user' : None,
                'host' : None,
        }
        self.method, self.nickid = self.find_nick(nick, user, host)
        if self.method == 'nick' or self.method == 'alias':
            self.host = self.check_host(user, host)
        else:
            self.host = True
        self.__conn_des(hash)
    
    def party_done(self):
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        query = '''INSERT INTO nick_channels ( nickid, channelid )
            VALUES ( :nickid, :channelid );'''
        data = {
            'nickid' : self.nickid,
            'channelid' : self.data['channelid'],
        }
        cursor.execute(query, data)
        self.conn.commit()
        self.__conn_des(hash)

    def was_in(self, channel):
        hash = self.__conn_init()
        channelid = self.find_channel(channel)
        cursor = self.conn.cursor()
        query = '''SELECT nickid, channelid
            FROM nick_channels
            WHERE nickid = :nickid
            AND channelid = :channelid ;'''
        data = {
            'nickid' : self.nickid,
            'channelid' : channelid,
        }
        cursor.execute(query, data)
        was = cursor.fetchone()
        self.__conn_des(hash)
        if was:
            return True
        else:
            return False

        #find channelid
    def find_channel(self, channel):
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        
        # pull channel
        query = '''SELECT channelid, channel
            FROM channels
            WHERE channel = :channel;'''
        data = {
            'channel' : channel
        }
        cursor.execute(query, data)
        channel = cursor.fetchone()
        if not channel: #we haven't seen anyone on this channel
            query = '''INSERT INTO channels ( channel )
                VALUES ( :channel );''';
            cursor.execute(query, data)
            self.conn.commit()
            channelid = cursor.lastrowid
        else:
            channelid = channel[0]
        self.data['channel'] = channel
        self.data['channelid'] = channelid
        self.__conn_des(hash)
        return channelid

        # find nick
    def find_nick(self, nick, user, host):
        nick_id = None
        nick_id = self.find_by_nick(nick)
        if nick_id:
            return 'nick',nick_id
        nick_id = self.find_by_alias(nick)
        if nick_id:
            return 'alias', nick_id
        nick_id = self.find_by_host(user, host)
        if nick_id:
            return 'host', nick_id
        return 'new', self.new_nick(nick, user, host)

    def find_by_nick(self, nick): #return nickid
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        # pull a row by nick
        query = '''SELECT nickid, nick 
            FROM nicks 
            WHERE nick = :nick ;'''
        data = {
            'nick' : nick
        }
        cursor.execute(query, data)
        nick = cursor.fetchone()
        self.__conn_des(hash)
        if nick: #cool, we have something
            self.data['nick'] = nick[1]
            self.data['nickid'] = nick[0]
            return nick[0]
        else:
            return None

    def find_by_alias(self, alias): #return nickid
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        query = '''SELECT nickid, alias, nick
            FROM aliases
            JOIN nicks USING(nickid)
            WHERE alias = :alias ;'''
        data = {
            'alias' : alias
        }
        cursor.execute(query, data)
        alias = cursor.fetchone()
        self.__conn_des(hash)
        if alias:
            self.data['nick'] = alias[2]
            self.data['nickid'] = alias[0]
            return alias[0]
        else:
            return None

    def find_by_host(self, user, host): #return nickid
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        query = '''SELECT nickid, nick, hostid, user, host
            FROM hosts
            JOIN nick_hosts USING(hostid)
            JOIN nicks USING(nickid)
            WHERE user = :user
            AND host = :host ;'''
        data = {
            'user' : user,
            'host' : host,
        }
        cursor.execute(query, data)
        host = cursor.fetchone()
        self.__conn_des(hash)
        if host:
            self.data['nick'] = host[1]
            self.data['nickid'] = host[0]
            self.data['hostid'] = host[2]
            self.data['user'] = host[3]
            self.data['host'] = host[4]
            return host[0]
        else:
            return None

    def new_nick(self, nick, user, host): #return nickid
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        query = '''INSERT INTO nicks ( nick )
            VALUES ( :nick );'''
        data = {
            'nick' : nick
        }
        cursor.execute(query, data)
        self.conn.commit()
        nickid = cursor.lastrowid

        query = '''INSERT INTO hosts ( user, host )
            VALUES ( :user, :host );'''
        data = {
            'user' : user,
            'host' : host,
        }
        cursor.execute(query, data)
        self.conn.commit()
        hostid = cursor.lastrowid

        query = '''INSERT INTO nick_hosts ( nickid, hostid )
            VALUES ( :nickid, :hostid );'''
        data = {
            'nickid' : nickid,
            'hostid' : hostid,
        }
        cursor.execute(query, data)
        self.conn.commit()

        self.data['nickid'] = nickid
        self.data['nick'] = nick
        self.data['hostid'] = hostid
        self.data['user'] = user
        self.data['host'] = host
        self.__conn_des(hash)   
        return nickid

    def check_host(self, user, host):
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        query = '''SELECT hostid, user, host
            FROM hosts
            JOIN nick_hosts USING ( hostid )
            WHERE host = :host
            AND nickid = :nickid'''
        data = {
            'host' : host,
            'nickid' : self.nickid,
        }
        cursor.execute(query, data)
        nick_host = cursor.fetchone()
        self.__conn_des(hash)
        if nick_host:
            self.data['hostid'] = nick_host[0]
            self.data['user'] = nick_host[1]
            self.data['host'] = nick_host[2]
            return True
        else:
            return False

    def add_alias(self, alias):
        if re.compile('('+')|('.join(self.__ignore)+')').match(alias):
            return
        if alias == self.data['nick']:
            return
        hash = self.__conn_init()
        cursor = self.conn.cursor()
        if self.method == 'host' : #we found the nick by host and then he switches to his usual nick
            if self.data['nick'] != alias: #his new nick isn't the same as his nick attached to host
                query = '''SELECT *
                    FROM aliases
                    WHERE alias = :alias
                    AND nickid = :nickid;'''
                data = {
                    'alias' : alias,
                    'nickid' : self.data['nickid'],
                }
                cursor.execute(query, data)
                ali = cursor.fetchon()
                if ali: # We recognized him!
                    alias = self.nick
            else: #same nick as attached to host
                alias = self.nick
        query = '''SELECT alias
            FROM aliases
            WHERE alias = :alias
            AND nickid = :nickid ;'''
        data = {
            'alias' : alias,
            'nickid' : self.nickid,
        }
        cursor.execute(query, data)
        aliases = cursor.fetchone()
        if not aliases:
            query = '''INSERT INTO aliases ( nickid, alias )
                VALUES ( :nickid, :alias );'''
            cursor.execute(query, data)
            self.conn.commit()
        self.__conn_des(hash)


def setup(phenny):
    phenny.party_db = os.path.join(os.path.expanduser('~/.phenny'), 'party.db')
    phenny.party_conn = sqlite3.connect(phenny.party_db)

    c = phenny.party_conn.cursor()
    c.execute('''PRAGMA foreign_keys = ON;''')
    c.execute('''CREATE TABLE IF NOT EXISTS nicks(
        nickid      INTEGER PRIMARY KEY NOT NULL,
        nick        VARCHAR(255) NOT NULL,
        UNIQUE(nick) ON CONFLICT IGNORE
    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS channels(
        channelid   INTEGER PRIMARY KEY NOT NULL,
        channel     VARCHAR(255) NOT NULL,
        UNIQUE(channel) ON CONFLICT IGNORE
    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS aliases(
        nickid      INTEGER NOT NULL,
        alias       VARCHAR(255) NOT NULL,
        FOREIGN KEY(nickid) REFERENCES nicks(nickid)
    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS hosts(
        hostid      INTEGER PRIMARY KEY,
        user        VARCHAR(255) NOT NULL,
        host        VARCHAR(255) NOT NULL,
        UNIQUE(user, host) ON CONFLICT IGNORE
    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS nick_hosts(
        nickid      INTEGER NOT NULL,
        hostid      INTEGER NOT NULL,
        FOREIGN KEY(nickid) REFERENCES nicks(nickid) ON DELETE CASCADE,
        FOREIGN KEY(hostid) REFERENCES hosts(hostid) ON DELETE CASCADE,
        UNIQUE(nickid, hostid) ON CONFLICT IGNORE
    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS nick_channels(
        nickid      INTEGER NOT NULL,
        channelid   INTEGER NOT NULL,
        FOREIGN KEY(nickid) REFERENCES nicks(nickid) ON DELETE CASCADE,
        FOREIGN KEY(channelid) REFERENCES channels(channelid) ON DELETE CASCADE,
        UNIQUE(nickid,channelid) ON CONFLICT IGNORE
    );''')
    c.close()
    phenny.party_conn.commit()
    print(phenny.party_db)
setup.thread = False


def on_join(phenny, input):
	party_channels = []
	try:
		party_channels = phenny.config.party
	except:
		return # if no one configured channels to party in, let's not start throwing parties
    if input in party_channels:
        nick = PartyGoer(phenny, input.nick, input.user, input.host)
        if nick.method == 'host': #found by hostname only, that doesn't say much
            phenny.say("Have I seen you before, %s?"%(input.nick))
            phenny.say("Oh! Oh! Are you %s?"%(nick.data['nick']))
            return
        if nick.was_in(input) :
            return
        else:
            party(phenny, nick)
            nick.party_done()

on_join.event = 'JOIN'
on_join.rule = r'.*'
on_join.thread = False

def on_nick(phenny, input):
    nick = PartyGoer(phenny, input.nick, input.user, input.host)
    if nick:
        nick.add_alias(input.sender)
    else:
        nick = PartyGoer(input.sender, input.user, input.host)

on_nick.event = 'NICK'
on_nick.rule = r'.*'
on_nick.thread = False

def party(phenny, nick):
    if nick in vip:
        vip_party(phenny, nick)
    else:
        # Normal party!
        phenny.say('Hey! I haven\'t seen you around here before! That must mean you\'re new!')
        phenny.do('brings out the party cannon for {0}!'.format(nick))
        phenny.say('So, here\'s your welcome party! Woo!')

def vip_party(phenny, nick):
    phenny.say('Hey! I haven\'t seen you around here before! That must mean you\'re new!')
    phenny.do('brings out the party cannon for {0}!'.format(nick))
    phenny.say('So, here\'s your welcome party! Woo!')
    phenny.msg(nick, 'And you get an extra special welcome!')
    phenny.msg(nick, '\x01ACTION licks her lips and pushes {0} to the ground, grinning above them. She then licks their cheek and nibbles lightly on their ear, giggling loudly.\x01'.format(nick))
    phenny.msg(nick, 'Maybe next time we can have a lot more fun. Sound good?')
    return
