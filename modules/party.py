#!/usr/bin/python3
'''
party.py - Pinkie's new nick greeting module
(C) 2012 Jordan Kinsley <jordan@jordantkinsley.org>
GPLv2 or later

This module checks for when a new nick joins the channel, and if the nick 
hasn't been seen before, she will throw them a party. 
'''

import os, sqlite3, re

#These ponies get Pinkie's VIP party. :3c
vip = ('Kinsley','Cocoa','MalevolentSpoon','TiredFoal','Aurora','Lapsus','Thorinair','Izia','Shutter')

def setup(self):
    self.party_db = os.path.join(os.path.expanduser('~/.phenny'), 'party.db')
    self.party_conn = sqlite3.connect(self.party_db)

    c = self.party_conn.cursor()
    c.execute('''create table if not exists nicks(
		channel		varchar(255),
		nick		varchar(255),
		unique(nick) on conflict replace
    );''')
    c.close()
    self.party_conn.commit()
setup.thread = False

def check_nick(channel, nick):
    seen = False
    sqlitedata = {
        'channel': channel,
        'nick': nick,
    }
    if not check_nick.conn:
        check_nick.conn = sqlite3.connect(phenny.party_db)
    
    c = check_nick.conn.cursor()
    c.execute('''select nick from nicks where channel = :channel and nick = :nick;''', sqlitedata)
    
    return seen
check_nick.conn = None
check_nick.thread = False

def on_join(phenny, input):
    channel = input.sender
    nick = input.nick
    if check_nick(channel, nick):
        return
    else:
        party(phenny, input)
        seen_nick(channel, nick)
on_join.event = 'JOIN'
on_join.rule = r'.*'
on_join.thread = False


def party(phenny, input):
    nick = input.nick
    if nick in vip:
        vip_party(phenny, input)
    else:
        # Normal party!
        phenny.say('Hey! I haven\'t seen you around here before! That must mean you\'re new!')
        phenny.action('brings out the party cannon for {0}!'.format(nick)
        phenny.say('So, here\'s your welcome party! Woo!')

def vip_party(phenny, input):
    nick = input.nick
    phenny.say('Hey! I haven\'t seen you around here before! That must mean you\'re new!')
    phenny.action('brings out the party cannon for {0}!'.format(nick)
    phenny.say('So, here\'s your welcome party! Woo!')
    phenny.msg(nick, 'And you get an extra special welcome!')
    phenny.msg(nick, '\x01ACTION licks her lips and pushes {0} to the ground, grinning above them. She then licks their cheek and nibbles lightly on their ear, giggling loudly.\x01'.format(nick))
    phenny.msg(nick, 'Maybe next time we can a lot more fun. Sound good?')
    return

def seen_nick(channel, nick):
    sqlitedata = {'channel': channel, 'nick': nick,}
    if not seen_nick.conn:
        seen_nick.conn = sqlite3.connect(phenny.party_db)
    
    c = seen_nick.conn.cursor()
    #c.execute insert
seen_nick.thread = False
seen_nick.conn = None
