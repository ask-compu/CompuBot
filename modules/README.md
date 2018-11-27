Modules
-------

The following modules have been modified for Pinkie or outright created for Pinkie. 

img.py
======

Stores "images" in an SQLite database for later retrieval with a command. Changes can be made either by an admin or by the nick who submitted the original image.
Images are actually image links; phenny did not support DCC file transfers at the time and implementing that feature would have been more trouble than it was worth for the purposes of this module. 
Current bugs: SQLite has poor support for threading, therefore all commands and functions **MUST** explicity include the `thread = false` directive at the end (in addition to any command and variable directives).
`getall` might currently be broken; I have not fully tested img.py recently. 

ping.py
=======

This module originally included a few commands to verify that phenny/pinkie was currently connected (i.e. not pinging out) and responding to commands. 
With help from Amos' (Amos on irc.caffie.net/#Equestria) changes, Pinkie has gained a huge number of "character" commands and responses. Attention has been paid to making Pinkie seem "in-character", except in certain cases of giving certain nicks special responses. These special responses have somewhat inspired the party.py module.
Current bugs: None, as far as I am aware. A user-level "bug" might be that not all actions are currently implemented, but more features are always being written. Features are written based on percieved need (i.e. a user performs an action to Pinkie, but she currently has no response for that action).

rule34.py
=========

This module was originally meant to query the site rule34.xxx, a hentai "booru"-style imageboard. Since the imageboard software is largely similar (if not the same), it was trivial to add additional functions to query the furry site e621.net and the FiM site twentypercentcooler.net (ponibooru and derpybooru were not included in this module because of ponibooru's poor site performance and the author's ignorance of derpybooru).
In addition to querying these new sites, additional code was added to properly filter actual NSFW links from SFW links via the board's build-in Rating system ("Safe","Questionable","Explicit"). 
Current bugs: Again, none, as far as I am aware. A user-level "bug" is that each board requires the proper knowledge of how its tag system works, i.e. if a user wishes to find images of Rarity, the My Little Pony character, on e621.net, they must search "Rarity\_(mlp)".
Code submitted by Kazunekit (Kazune on irc.canternet.org/#fic) refactors much of the shared code for the Ouroborus sites (e621, e926, and twentypercentcooler) as well as the performance improvement of using the XML API of rule34.xxx.

head.py
=======

Another module that has been extended for FiM-specific sites. If it detects a FimFiction.net story link (a link that looks like `http://fimfiction.net/story/<story-id>/<story-name>`), it skips the normal page title code and reads the info from the story page, gathering the story name, author, likes, dislikes, and, calculated from the likes and dislikes, the overall percentage rating.
Also, some code submitted by Polarfire (Polarfire on irc.canternet.org/#techponies) allows for similar information from Youtube links, whether they be the short youtu.be/<vid> style or the regular youtube.com/watch?v=<vid> style (should be able to find the video ID in the other URL decorators).
Information gathered includes video title, view count, duration, and uploader. May be extended to include likes, dislikes, and percentage.
Code submitted by Kazunekit (Kazune on irc.canternet.org/#fic) allows for greater use of imageboards with some code refactoring and additional titling features. 
Fixed a bug caused by e621 likely blocking scripts' User-agent strings; the higher-level web.py module was changed to handle HTTPErrors by switching to a different method of openning the URL by faking the User-agent in the header. Regrettable, but just swallowing errors and not having titles for e621 links wasn't a long term solution. 

party.py
========

This original module is designed to greet new nicks when they join the channel, and, if they are on the "VIP list", private message an additional, special greeting. (The VIP function is most for an inside joke and can be safely ignored.)
Current bugs: **CRITICAL** Pinkie will issue a greeting for any new _nick_, meaning that if a user changes their nick and Pinkie has not seen it, she will issue a new greeting. To prevent this, it would be most beneficial to get the complete hostmask of the user in question and only issue a new greeting if their hostmask is unique. Additional code for allowing new IP masks (i.e., look at the larger ISP hostname or IP block and not the unique IP) should be required.

admin.py
========

Code was added in the admin.py module to allow for a server-side ignore on the Canternet network using the /SILENCE command. This code is largely untested and may not function correctly. Additional testing is needed. Current bugs: Unknown.

info.py
=======

Made changes to bring the info up to date with Pinkie's current status. Added a .source/.github command so Pinkie will tell people about her code and the link to the Github repo.
