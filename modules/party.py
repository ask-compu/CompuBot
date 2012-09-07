#!/usr/bin/python3
'''
party.py - Pinkie's new nick greeting module
(C) 2012 Jordan Kinsley <jordan@jordantkinsley.org>
GPLv2 or later

This module checks for when a new nick joins the channel, and if the nick 
hasn't been seen before, she will throw them a party. 
'''

import os, sqlite3, re

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
    # TODO: look up nick in the DB
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
    phenny.say(str(input.groups()))
on_join.event = 'JOIN'
on_join.rule = r'.*'
on_join.thread = False
