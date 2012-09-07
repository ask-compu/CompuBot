#!/usr/bin/python3
'''
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/

Modified from ping.py by Amos

Modified by Jordan Kinsley <jordan@jordantkinsley.org>
'''

import random

saucyreplies = ('Kinsley','MalevolentSpoon','Aurora','Cocoa','TiredFoal','Lapsus')

def hello(phenny, input): 
    greeting = random.choice(('Hi', 'Hey', 'Hello'))
    punctuation = random.choice(('.', '!'))
    phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) (I|Bli|Pi)nkie(Pie)?(Bot)?\b'

def sniff(phenny, input): 
    sniffresponse = random.choice(('Hey! Do I know you?', 'Umm...', 'Do I smell funny - like \'haha\' funny or \'funny\' funny?', 'EEP!', 'ACTION prods ' + input.nick + '\'s nose.'))
    phenny.say(sniffresponse)
sniff.rule = r'(?i)(ACTION sniffs (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def grope(phenny, input): 
    groperesponse = random.choice(('I love hugs!', 'ACTION hugs ' + input.nick + ' SUPER hard.', 'ACK!', 'Hahaha, you suprised me, ' + input.nick + '!', 'Gasp!'))
    phenny.say(groperesponse)
grope.rule = r'(?i)(ACTION runs over and squeezes (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def flirt(phenny, input): 
    attractresponse = '.'
    if input.nick in saucyreplies:
        attractresponse = random.choice(('Well, hey there, cutie. ;)','Such a flirt!','ACTION pounces ' + input.nick + '.','ACTION winks at ' + input.nick + '.'))
    else: 
        attractresponse = random.choice(('I don\'t like you that way...', 'Sorry, I\'m not like that.', 'Flattering, but no.', 'Are you trying to flirt with me?', 'I\'d rather just be friends.', '...'))
    phenny.say(attractresponse)
flirt.rule = r'(?i)(ACTION winks at (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def lick(phenny, input): 
    lickresponse = '.'
    if input.nick in saucyreplies:
        lickresponse = random.choice(('ACTION blushes.', 'ACTION pounces ' + input.nick + '.', 'ACTION steals ' + input.nick + '\'s virginity.', 'Hee... We better take this elsewhere...','Ooooh!'))
    else:
        lickresponse = random.choice(('...', 'What do I taste like? I want to know!', 'Ah!', 'Eep!', 'That tickles!', 'ACTION licks ' + input.nick + ' right back.', 'I don\'t like you that way...', 'Eww...','Waugh...', 'Ah!', '!', 'ACTION blushes.', 'ACTION pounces ' + input.nick + '.', 'ACTION steals ' + input.nick + '\'s virginity.', 'Hehe...'))
    phenny.say(lickresponse)
lick.rule = r'(?i)(ACTION licks (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def growl(phenny, input): 
    # TODO: add more responses
    growlresponse = random.choice(('Silly puppy!', 'ACTION gives ' + input.nick + ' a slice of cake.', 'What did I do?', 'ACTION growls back.', 'Something wrong?'))
    phenny.say(growlresponse)
growl.rule = r'(?i)(ACTION growls at (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def kiss(phenny, input):
    kissresponse = '.'
    if input.nick in saucyreplies:
        kissresponse = random.choice(('ACTION blushes.', 'ACTION pounces ' + input.nick + '.', 'ACTION steals ' + input.nick + '\'s virginity.', 'Hee... We better take this elsewhere...','Ooooh!','ACTION kisses ' + input.nick + ' back.','ACTION pushes ' + input.nick + ' to the ground and ravishes them.'))
    else:
        kissresponse = random.choice(('ACTION blushes','What was that for?','ACTION leaps into the air in suprise.', 'ACTION pushes ' + input.nick + ' away.', 'ACTION bucks ' + input.nick + ' in the chest. Hard.', 'ACTION giggles.'))
    phenny.say(kissresponse)
kiss.rule = r'(?i)(ACTION kisses (I|Bli|Pi)nkie(Pie)?(Bot)?)'

def interjection(phenny, input): 
    phenny.say(input.nick + '!')
interjection.rule = r'(I|Bli|Pi)nkie(Pie)?(Bot)?!'
interjection.priority = 'high'
interjection.thread = False

def hugs(phenny, input):
    hugresponse = random.choice(('ACTION hugs ' + input.nick + ' back.', 'ACTION giggles.', 'Thanks, ' + input.nick + ', that felt really good!', 'Hugs for everypony!'))
    phenny.say(hugresponse)
hugs.rule = r'(ACTION)? (?i)(hugs) (?i)(I|Bli|Pi)nkie(Pie)?(Bot)?'

def tickles(phenny, input):
    tickleresponse = '.'
    if input.nick in saucyreplies:
        tickleresponse = random.choice(('Hehehe! That tickles!', 'ACTION rolls on the floor, laughing.','EEP!','ACTION gigglesnorts','ACTION rolls ' + input.nick + ' over and tickles them back!','ACTION declares a tickle war!','ACTION giggles and pushes ' + input.nick + ' to the floor and kisses them.', 'ACTION giggles and takes ' + input.nick + '\'s hoof, and leads them to private room.'))
    else:
        tickleresponse = random.choice(('Hehehe! That tickles!', 'ACTION rolls on the floor, laughing.','EEP!','ACTION gigglesnorts','ACTION rolls ' + input.nick + ' over and tickles them back!','ACTION declares a tickle war!'))
    phenny.say(tickleresponse)
tickles.rule = r'(ACTION)? (?i)(tickles) (?i)(I|Bli|Pi)nkie(Pie)?(Bot)?'

def parties(phenny, input):
    # TODO: add more responses
    partyresponse = random.choice(('Woo! A party!', 'ACTION invites the whole town to party!', 'ACTION grabs her emergency party supplies!', 'ACTION puts on some sweet jams!'))
    phenny.say(partyresponse)
parties.rule = r'(ACTION)? (?i)(parties with) (?i)(I|Bli|Pi)nkie(Pie)?(Bot)?'

def smiles(phenny, input):
    # ACTION smiles back! gets extra "weight" because it's a good response
    smilesresponse = random.choice(('Aww, I love to see my friends smile!','ACTION smiles back!','#youtubelink','ACTION grins!','ACTION claps her hooves together!','ACTION smiles back!'))
    phenny.say(smilesresponse)
smiles.rule = r'(ACTION)? (?i)smiles (?i)(at|with|to|because of) (?i)(I|Bli|Pi)nkie(Pie)?(Bot)?'

#TODO: create a "frowns" function with rule for "frownie" smilies and /me frowns.

def thanks(phenny, input):
    thanksresponse = random.choice(('No problemo', 'My pleasure', 'Hahah, you\'re welcome','I\'m always there for my friends'))
    thankspuncuation = random.choice(('!', '.'))
    phenny.say(thanksresponse + thankspuncuation)
thanks.rule = r'(?i)(Thank( you|s)?(,)? (I|Bli|Pi)nkie(Pie)?(Bot)?)'

# TODO: add these actions and appropriate responses
'''
Actions to add: 
(first to four stars get written, and any action with more than two at that time will be written as well)
* pokes **
* cupcakes *
* kicks *
* good night *
* pets *
* hoofshake **
* flank-smack *
* how are you *
* wallows on *
* gives a massage to *
* fondles/molests/gropes **
* random hugs (triggered via private message) 
'''

# action string 'ACTION'

if __name__ == '__main__': 
	print(__doc__.strip())
