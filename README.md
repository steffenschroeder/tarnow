Tarnow
======
[![Build Status](https://travis-ci.org/steffenschroeder/tarnow.svg?branch=master)](https://travis-ci.org/steffenschroeder/tarnow)

Tarnow is a front end for [rcswitch-pi](https://github.com/r10r/rcswitch-pi/). It consist of a responsive Flask Frontend and a wrapper
script to allow timed switches using cronjobs. All you need to know is the a


## Features
1. Use the crontab to automatically switch on / switch off 433MHz radio controlled switches
2. Skip next occurrence
3. Skip all occurrences
4. switch on / off all your switches at once

## Installation
1. Install a 433MHz sender to your raspberry pi (Data: pin 11 (GPIO 0), VCC: pin 2 (5V), GND: pin 6 (GND)
2. Install required packages: ``sudo apt-get install make gcc gcc-c++``
3. install wiringPi (See http://wiringpi.com/download-and-install/ for detailed install instructions)
    * ``git clone git://git.drogon.net/wiringPi``
    * go to directory wiringPi
    * run `./build`
 4. install rcswitch-pi (see also https://github.com/r10r/rcswitch-pi/)
    * ``git clone https://github.com/r10r/rcswitch-pi.git``
    * go to directory rcswitch-pi
    * execute ``make`` (this creates a _send_ executable) in the cloned repository
    * ``sudo cp send /usr/local/sbin/send433``
    * ``sudo chown root:root /usr/local/sbin/send433``
5. clone this repository
6. run ``sudo pip install -r requirements.txt``
7. adopt the config file (config.py) by adding your home code and the switches

## Usage
- To use the dev server, run ``python /home/pi/tarnow/tarnow.py`` to start the web server on port 8080.
- To use a production ready server, run ``sudo make serve`` (after you installed ``pip install gunicorn``)
- Open the url _http://ip:8080_ where _ip_ is the IP for your Raspberry Pi.
- run ``make switch <switchname>|all 0|1`` from command line or a cron job


## Build a timed switch using cron
The switches can be changed by using the script tarnow_switch.py <switch> 0|1
This is useful to run as timed switch using cron
Example (the switch 'radio' in defined in config.py:

```no-highlight
#everyday at 7am
0 7 * * * python3 /home/pi/tarnow/tarnow_switch.py  radio 1
# Monday to Friday at 9:15 am
15 9 * * mon-fri  python3 /home/pi/tarnow/tarnow_switch.py  radio 0
# Monday to Friday at 6:00 pm
0 18 * * mon-fri python3 /home/pi/tarnow/tarnow_switch.py  radio 1
# Sunday to Thursday 10:30 am
30 22  * * sun-thu python3 /home/pi/tarnow/tarnow_switch.py  radio 0
# turn off everyday at midnight
0 0 * * * python3 /home/pi/tarnow/tarnow_switch.py all 0
```
## HTTP API
You can use a HTTP GET request to control the switches and skips. This can be useful to build on top of _tarnow_. You can e.g. store a switch-off-all URL on an NFC Tag. Then just scan the tag with your smartphone, the URL opens and everything is off.
The format is like ``http://<ip>:8080/<command>/<parameter>``

| Command         | What is does                               | Parameter         | Example                                           |
|:----------------|:-------------------------------------------|:------------------|:--------------------------------------------------|
| on              | Enables a switch                           | a switch or _all_ | http://192.168.0.12:8080/on/Radio                 |
| off             | Disables a switch                          | a switch or _all_ | http://192.168.0.12:8080/off/all                  |
| createtemporary | Skip next automatic switch execution       | a switch          | http://192.168.0.12:8080/createtemporary/Internet |
| createpermanent | Skip all automatic switch executions       | a switch          | http://192.168.0.12:8080/createpermanent/TV       |
| deletetemporary | Don't skip next automatic switch execution | a switch          | http://192.168.0.12:8080/deletetemporary/Internet |
| deletepermanent | Don't skip all automatic switch execution  | a switch          | http://192.168.0.12:8080/deletepermanent/TV       |


## Autostart
To automatically start the server, add the following line to your ``/etc/rc.local``:
``python /home/pi/tarnow/tarnow.py &`` (or when using gunicorn  ``cd /home/pi/tarnow && sudo gunicorn --bind 0.0.0.0:8080 tarnow:app``)

## And finally: how it looks like
![Screenshot](https://raw.githubusercontent.com/steffenschroeder/tarnow/docu/screenshots/mobile.png)

Licensed under the [MIT License](http://en.wikipedia.org/wiki/MIT_License)
