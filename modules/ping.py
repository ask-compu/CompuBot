#!/usr/bin/python3
'''
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/

Modified from ping.py by Amos

Modified by Jordan Kinsley <jordan@jordantkinsley.org>
'''

import random

saucyreplies = ('Kinsley','MalevolentSpoon','Aurora','Cocoa','TiredFoal','Lapsus','Compu','Ace','Firestar','cloppyhooves','Connor','princesssluttershy','plushie_pegasus','IceFlurries','Shroo','Giggles','eytosh','iamalion','weisey','CompuDesktop')

def hello(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        phenny.say("Nope, you're in the naughty list!")
        return
    greeting = random.choice(('Hi', 'Hey', 'Hello'))
    punctuation = random.choice(('.', '!'))
    phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) (?i)CompuBot\b'

def sniff(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        return
    sniffresponse = random.choice(('Hey! Do I know you?', 'Umm...', 'Do I smell funny - like \'haha\' funny or \'funny\' funny?', 'EEP!', '\x01ACTION prods ' + input.nick + '\'s nose.\x01'))
    phenny.say(sniffresponse)
sniff.rule = r'(?i)(\x01ACTION sniffs (?i)CompuBot)'

def grope(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        return
    groperesponse = random.choice(('I love hugs!', '\x01ACTION hugs ' + input.nick + ' SUPER hard.\x01', 'ACK!', 'Hahaha, you suprised me, ' + input.nick + '!', 'Gasp!'))
    phenny.say(groperesponse)
grope.rule = r'(?i)(\x01ACTION runs over and squeezes (?i)CompuBot)'

def flirt(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        return
    attractresponse = '.'
    if input.nick in saucyreplies:
        attractresponse = random.choice(('Well, hey there, cutie. ;)','Such a flirt!','\x01ACTION pounces ' + input.nick + '.\x01','\x01ACTION winks at ' + input.nick + '.\x01'))
    else: 
        attractresponse = random.choice(('I don\'t like you that way...', 'Sorry, I\'m not like that.', 'Flattering, but no.', 'Are you trying to flirt with me?', 'I\'d rather just be friends.', '...'))
    phenny.say(attractresponse)
flirt.rule = r'(?i)(\x01ACTION winks at (?i)CompuBot)'

def lick(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        return
    lickresponse = '.'
    if input.nick in saucyreplies:
        lickresponse = random.choice(('\x01ACTION blushes.\x01', '\x01ACTION pounces ' + input.nick + '.\x01', '\x01ACTION steals ' + input.nick + '\'s virginity.\x01', 'Hee... We better take this elsewhere...','Ooooh!'))
    else:
        lickresponse = random.choice(('...', 'What do I taste like? I want to know!', 'Ah!', 'Eep!', 'That tickles!', '\x01ACTION licks ' + input.nick + ' right back.\x01', 'I don\'t like you that way...', 'Eww...','Waugh...', 'Ah!', '!', '\x01ACTION blushes.\x01', '\x01ACTION pounces ' + input.nick + '.\x01', '\x01ACTION steals ' + input.nick + '\'s virginity.\x01', 'Hehe...'))
    phenny.say(lickresponse)
lick.rule = r'(?i)(\x01ACTION licks (?i)CompuBot)'

def growl(phenny, input): 
    if input.nick in phenny.config.user_ignore:
        return
    # TODO: add more responses
    growlresponse = random.choice(('Silly puppy!', '\x01ACTION gives ' + input.nick + ' a slice of cake.\x01', 'What did I do?', '\x01ACTION growls back.\x01', 'Something wrong?'))
    phenny.say(growlresponse)
growl.rule = r'(?i)(\x01ACTION growls at (?i)CompuBot)'

def kiss(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    kissresponse = '.'
    if input.nick in saucyreplies:
        kissresponse = random.choice(('\x01ACTION blushes.\x01', '\x01ACTION pounces ' + input.nick + '.\x01', '\x01ACTION steals ' + input.nick + '\'s virginity.\x01', 'Hee... We better take this elsewhere...','Ooooh!','\x01ACTION kisses ' + input.nick + ' back.\x01','\x01ACTION pushes ' + input.nick + ' to the ground and ravishes them.\x01'))
    else:
        kissresponse = random.choice(('\x01ACTION blushes\x01','What was that for?','\x01ACTION leaps into the air in suprise.\x01', '\x01ACTION pushes ' + input.nick + ' away.\x01', '\x01ACTION bucks ' + input.nick + ' in the chest. Hard.\x01', '\x01ACTION giggles.\x01'))
    phenny.say(kissresponse)
kiss.rule = r'(?i)(\x01ACTION kisses (?i)CompuBot)'

def interjection(phenny, input): 
    phenny.say(input.nick + '!')
interjection.rule = r'(?i)CompuBot!'
interjection.priority = 'high'
interjection.thread = False

def hugs(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    hugresponse = random.choice(('\x01ACTION hugs ' + input.nick + ' back.\x01', '\x01ACTION giggles.\x01', 'Thanks, ' + input.nick + ', that felt really good!', 'Hugs for everypony!'))
    phenny.say(hugresponse)
hugs.rule = r'(\x01ACTION)? (?i)(hugs) (?i)CompuBot'

def tickles(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    tickleresponse = '.'
    if input.nick in saucyreplies:
        tickleresponse = random.choice(('Hehehe! That tickles!', '\x01ACTION rolls on the floor, laughing.\x01','EEP!','\x01ACTION gigglesnorts\x01','\x01ACTION rolls ' + input.nick + ' over and tickles them back!\x01','\x01ACTION declares a tickle war!\x01','\x01ACTION giggles and pushes ' + input.nick + ' to the floor and kisses them.\x01', '\x01ACTION giggles and takes ' + input.nick + '\'s hoof, and leads them to private room.\x01'))
    else:
        tickleresponse = random.choice(('Hehehe! That tickles!', '\x01ACTION rolls on the floor, laughing.\x01','EEP!','\x01ACTION gigglesnorts\x01','\x01ACTION rolls ' + input.nick + ' over and tickles them back!\x01','\x01ACTION declares a tickle war!\x01'))
    phenny.say(tickleresponse)
tickles.rule = r'(\x01ACTION)? (?i)(tickles) (?i)CompuBot'

def parties(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    # TODO: add more responses
    partyresponse = random.choice(('Woo! A party!', '\x01ACTION invites the whole town to party!\x01', '\x01ACTION grabs her emergency party supplies!\x01', '\x01ACTION puts on some sweet jams!\x01'))
    phenny.say(partyresponse)
parties.rule = r'(\x01ACTION)? (?i)(parties with) (?i)CompuBot'

def smiles(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    # \x01ACTION smiles back!\x01 gets extra "weight" because it's a good response
    smilesresponse = random.choice(('Aww, I love to see my friends smile!','\x01ACTION smiles back!\x01','#youtubelink','\x01ACTION grins!\x01','\x01ACTION claps her hooves together!\x01','\x01ACTION smiles back!\x01'))
    phenny.say(smilesresponse)
smiles.rule = r'(\x01ACTION)? (?i)smiles (?i)(at|with|to|because of) (?i)CompuBot'

def frowns(phenny, input):
    if input.sender in ['#reddit-clopclop']:
        return
    if input.nick in phenny.config.user_ignore:
        return
    # we're going to have a one-in-ten chance of Pinkie trying to cheer you up
    if random.randint(9,10) == 10:
        frownsresponse = random.choice(('Aww, don\'t be sad, ' + input.nick + ', I\'m here!','\x01ACTION hugs ' + input.nick + '\x01', 'Cheer up, ' + input.nick + ', all of your friends are here!'))
        phenny.say(frownsresponse)
frowns.rule = r'(:<|:C|D:|:x|:X)|(\x01ACTION (?i)frowns(.*))|:\(|:\'\('

def thanks(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    thanksresponse = random.choice(('No problemo', 'My pleasure', 'Hahah, you\'re welcome','I\'m always there for my friends'))
    thankspuncuation = random.choice(('!', '.'))
    phenny.say(thanksresponse + thankspuncuation)
thanks.rule = r'(?i)(Thank( you|s)?(,)? (?i)CompuBot)'

def pokes(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    pokesresponse = ('Yes?', 'Hiya!', 'Hey, ' + input.nick + '!', 'Do you need anything from me?', 'What\'s up?')
    phenny.say(random.choice(pokesresponse))
pokes.rule = r'(\x01ACTION)? (?i)pokes (?i)CompuBot'

def bestpony(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    bestponyresponse = random.choice(('I am!','Me!','I\'m best pony!','I\'m best robomare!','I\'m best mare!','It\'s Me! It\'s Me!'))
#    bestponypuncuation = random.choice(('!', '.'))
#    phenny.say(bestponyresponse + bestponypuncuation)
    phenny.say(bestponyresponse)
bestpony.rule = r'(?i)(CompuBot(:|,)? )?(who(\'s|s| is)) (the )?best (pony|robomare|mare)[\?]?'

def ping(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    pingresponse = random.choice(('Pong!','Pong!'))
#    pingpuncuation = random.choice(('!', '.'))
#    phenny.say(pingresponse + pingpuncuation)
    phenny.say(pingresponse)
ping.rule = r'(?i).(P|p)ing'


def boops(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    boopsresponse = random.choice(('\x01ACTION eeps at ' + input.nick + '\x01','nya!','\x01ACTION giggles\x01','\x01ACTION goes cross-eyed\x01','\x01ACTION giggles and goes cross-eyed\x01'))
    phenny.say(boopsresponse)
boops.rule = r'(\x01ACTION)?( "accidentally"| trips and accidentally| sticks her tongue out and| gently| tries to)? (?i)boop(s)? (?i)CompuBot'

def cookie(phenny, input):
    if input.nick in phenny.config.user_ignore:
        return
    # we're going to have a one-in-ten chance of Pinkie trying to cheer you up
    if random.randint(9,10) == 10:
        cookieresponse = random.choice(('\x01ACTION gives ' + input.nick + ' a cookie\x01','\x01ACTION gives ' + input.nick + ' two cookies and milk\x01', '\x01ACTION throws five cookies in ' + input.nick + "'s direction\x01", '\x01ACTION gives ' + input.nick + ' a raisin and oat cookie'))
        phenny.say(cookieresponse)
cookie.rule = r'(?i)((CompuBot(:|,)? )?(C|c)ookies (P|p)lease(\?)?)|(?i)((CompuBot(:|,)? )?(((C|c)an (I|i))|((I|i) (C|c)an)) (((H|h)ave)|((H|h)as)) (C|c)ookie(s)?( (P|p)lease)?(\?)?)'

#def boopcommand(phenny, input):
#    if input.nick in phenny.config.user_ignore:
#        return
#    boopcommandresponse = random.choice(('\x01ACTION boops '))
#    phenny.say(boopcommandresponse)
#boopcommand.rule = (r'(?i)(CompuBot(:|,)? )?boop [^\s]+')

# TODO: add these actions and appropriate responses
'''
Actions to add: 
(first to four stars get written, and any action with three or more at that time will be written as well)
* cupcakes *
* kicks *
* good night *
* pets **
* hoofshake **
* flank-smack *
* how are you *
* gives a massage to *
* fondles/molests/gropes **
'''

# action string '\x01ACTION\x01'

if __name__ == '__main__': 
	print(__doc__.strip())
