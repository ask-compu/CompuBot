'''
boru.py - ignore_tags list for Ouroboros sites like e621.net, e926.net and twentypercentcooler.net
Initial list by Kazunekit
Additions and formatting by JordanKinsley

Copyright (C) 2013 by JordanKinsley
Licensed under the Eiffel Forum License 2.
'''

# a list of regular expressions to substitute out of the list of tags.
ignore_tags = [
	'artist:(\S*)',
	'bed',
	'blanket',
	'fur',
	'blue(\S*)',
	'candle',
	'safe',
	'questionable',
	'explicit',
	'duo',
	'equine',
	'female',
	'feral',
	'friendship_is_magic',
	'horse',
	'horn',
	'my_little_pony',
	'plain_background',
	'two_tone_hair',
	'unicorn',
	'white(\S*)',
	'black(\S*)',
	'looking_at_viewer',
	'[0-9][0-9][0-9][0-9]',
	'text',
	'english_text',
	'dialogue',
	'oddly_sexy',
	'smile',
	'wings',
	'(\S*)_eyes'
]