Tarnow
======
[![Build Status](https://travis-ci.org/steffenschroeder/tarnow.svg?branch=master)](https://travis-ci.org/steffenschroeder/tarnow)

Tarnow is a wrapper and a front end for raspberry-remote. It consist of a responsive Flask Frontend and a wrapper 
script to allow timed switches using cron.   


## Features
1. Use the crontab to automatically switch on / switch off 433MHz radio controlled switches
2. Skip next occurrence 
3. Skip all occurrences

## Installation
1. Install a 433MHz sender to your raspberry pi (Data: pin 11 (GPIO 0), VCC: pin 2 (5V), GND: pin 6 (GND)
2. Install required packages: ``sudo apt-get install make gcc gcc-c++``
3. install wiringPi (See http://wiringpi.com/download-and-install/ for detailed install instructions)
    * ``git clone git://git.drogon.net/wiringPi``
    * run `./build``
 
4. install raspberry remote (see also http://xkonni.github.io/raspberry-remote/)
    * ``git clone git://github.com/xkonni/raspberry-remote.git``
    * execute _make send_ (this creates a _send_ executable) in the cloned repository
    * ``sudo cp send /usr/local/sbin/send433``
    * ``sudo chown root:root /usr/local/sbin/send433``
5. clone this repository 
6. run ``sudo pip install -r requirements.txt``      
7. adopt the config file (config.py) by adding your home code and the switches
8. run ``python /home/pi/tarnow/tarnow.py`` to start the web server on port 8080


## Build a times switch using cron
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
0 0 * * * python3 /home/pi/tarnow/tarnow_switch.py  radio 0
```

## Autostart
To automatically start the server, add the following line to your ``/etc/rc.local``: 
``python /home/pi/tarnow/tarnow.py &``

Licensed under the [MIT License](http://en.wikipedia.org/wiki/MIT_License)
