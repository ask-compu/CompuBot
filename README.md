CompuBot
======

This is a port of phenny, a Python IRC bot, to Python3. It has been forked from [JordanKinsley](https://github.com/JordanKinsley)'s [PinkiePyBot](https://github.com/JordanKinsley/PinkiePyBot) port.

New features include many modifications to modules.

Compatibility with existing phenny modules has been mostly retained, but they
will need to be updated to run on Python3 if they do not already. All of the
core modules have been ported. 

Requirements
------------

CompuBot runs on a Ubuntu 14.04 LTS server and therefore doesn't get tested on other platforms*. You will need the latest version of Python 3.4 (which can be installed with `sudo apt-get install python3-all python3-all-dev`). Due to a new feature of lists, it is recommended that Python 3.3 or later be used. It is not required, but highly recommended. We thankfully no longer require the use of lxml or BeautifulSoup thanks to the JSON APIs of several sites. 

* CompuBot can run on Windows as long as Python 3.2 or later is installed. It's recommended to use the lastest version of Python to avoid the issues described above. 

Installation
------------
1. Run `./phenny` - this creates a default config file
2. Edit `~/.phenny/default.py`
3. Run `./phenny` - this now runs pinkie with your settings

Enjoy!

Already using CompuBot and upgrading?
----------------------------------------

New changes to some configuration options may mean you need to edit your default.py file to include new options. 

**rule34.py users:**
```python
# works like the channels config option, but defines what channels NSFW 
# material can be searched for. See rule34.py for more details
nsfw = ['#nsfw-example','#my-test-channel']
```

**Module developers:**
```python
# set to True to output detailed info about the actual traffic to and from the IRC server
debug = False
```

**All users:**
```python
# ignore these users. At the moment, the ignore is exact, but admin.py 
# has new commands to change config options at run time
user_ignore = ['anon','abuser']
```

Authors
-------
* Sean B. Palmer, http://inamidst.com/sbp/
* mutantmonkey, http://mutantmonkey.in
* Jordan Kinsley, http://jordantkinsley.org
