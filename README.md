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

pinkie runs on a Ubuntu 12.04 LTS server and therefore doesn't get tested on other platforms. You will need the latest version of Python 3.2 (which can be installed with sudo apt-get install python3-all python3-all-dev). If you are going to use the rule34.py paacke, you will also need the build-essential pseudo-package and the build dependancies for the python-lxml package (which can be installed with sudo apt-get install build-esstential && sudo apt-get build-dep python-lxml). The distrubtion provided python-lxml package does not provide the lxml.html module required by rule34.py. Installation instructions for lxml can be found at their [website](http://lxml.de/installation.html).

To get a fully-running pinkie, you need to run
    sudo apt-get install python3-all python3-all-dev build-essential
    sudo apt-get build-dep python-lxml
And download the latest stable version of lxml and install it with
    python3 setup.py build
    sudo python3 setup.py install

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
