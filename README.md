pinkie
======

This is a port of phenny, a Python IRC bot, to Python3. It has been forked from [mutantmonkey](https://github.com/mutantmonkey)'s [phenny](https://github.com/mutantmonkey/phenny) port.

New features include many new modules, IPv6 and TLS support (which requires
Python 3.2).

Compatibility with existing phenny modules has been mostly retained, but they
will need to be updated to run on Python3 if they do not already. All of the
core modules have been ported. 

Requirements
------------

pinkie runs on a Ubuntu 12.04 LTS server and therefore doesn't get tested on other platforms. You will need the latest version of Python 3.2 (which can be installed with `sudo apt-get install python3-all python3-all-dev`). We thankfully no longer require the use of lxml or BeautifulSoup thanks to the JSON APIs of several sites. 

Installation
------------
1. Run `./pinkie` - this creates a default config file
2. Edit `~/.pinkie/default.py`
3. Run `./pinkie` - this now runs pinkie with your settings

Enjoy!

Authors
-------
* Sean B. Palmer, http://inamidst.com/sbp/
* mutantmonkey, http://mutantmonkey.in
* Jordan Kinsley, http://jordantkinsley.org
