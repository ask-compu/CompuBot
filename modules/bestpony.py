#!/usr/bin/env python
'''
bestpony.py - PinkiePyBot best pony tracker
(C) 2012 Jordan T Kinsley (jordan@jordantkinsley.org)
GPLv2 or later

This module will let Pinkie inform users of the best pony or confirm or
deny their suspected best ponies. 
'''

import random, re

ponies = ('Twilight Sparkle','Rarity','Me','Applejack','Fluttershy','Sunset Shimmer')
ponies_alt = ('Princess Celestia','Princess Luna','Princess Cadance','Shining Armor','Roseluck','Trixie','Sweetie Belle','Apple Bloom','Scootaloo','Mr Cake','Mrs Cake','Pound Cake','Pumpkin Cake','Granny Smith','Big Macintosh','Lyra','Bon Bon')
not_best_ponies = ('Flash Sentry')
not_ponies = ('Discord','Philomena','Spike','Gilda','Gummy')
pony_map = {'Twilight': 'Twilight Sparkle', 'Celestia': 'Princess Celestia', 'Luna': 'Princess Luna', 'Cadance': 'Princess Cadance', 'Mr. Cake': 'Mr Cake', 'Mrs. Cake': 'Mrs Cake', 'Big Mac': 'Big Macintosh'}

def best_pony(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    best_pony_response = "Oh, that's easy, it's " + random.choice(ponies_alt) + "! No... wait, it's definitely " + random.choice(ponies) + "! "
    phenny.say(best_pony_response)
    phenny.say("I'm kidding, of course! It's you, silly!")
best_pony.rule = r'(?i)(I|Bli|Pi)nkie(Pie)?(Bot)?, who(\'s| is)( the)? best pony(\?)?'

def is_best_pony(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    rule_text = input.group(0) # unfortunately, unlike the image.py module, 
    # we're just using a rule, not a command. All of our input is in group 0
    find_pony = re.compile("(?i)(I|Bli|Pi)nkie(Pie)?(Bot)?, is (?P<pony>.*)( the)? best pony(\?)?")
    alleged_best_pony = re.match(find_pony, rule_text).group('pony').title()
    if alleged_best_pony in pony_map:
        alleged_best_pony = pony_map[alleged_best_pony]
    if alleged_best_pony == 'Rainbow Dash':
        phenny.say("Ha ha, yeah! Dashie's pretty cool.")
    elif alleged_best_pony == 'Pinkie Pie':
        phenny.say("Aw, that's sweet, " + input.nick + "! I think I'm pretty swell, too.")
    elif alleged_best_pony in ponies:
        phenny.say("Ha ha, yeah! " + alleged_best_pony + " is my best friend! I love her!")
    elif alleged_best_pony in ponies_alt:
        phenny.say("Ha ha, yeah! " + alleged_best_pony + " is pretty cool!")
    elif alleged_best_pony in not_ponies:
        phenny.say("Ha ha, you're silly! " + alleged_best_pony + " isn't a pony!")
    elif alleged_best_pony in not_best_ponies:
        phenny.say("Erm... no. No way! " + alleged_best_pony + " is totally not cool.")
    else:
        phenny.say("I'm sorry, " +  input.nick + " but I don't know " + alleged_best_pony + " very well. I'm sure they're pretty neat!")
    
is_best_pony.rule = r'(?i)(I|Bli|Pi)nkie(Pie)?(Bot)?, is (?#pony)(.*)( the)? best pony(\?)?'
