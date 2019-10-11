import pytest

__author__ = 'mav'

from tarnow import next_execution
import crontab
from datetime import datetime

CRONTAB = """
#everyday at 7am
15 7 * * mon-sat python3 /home/pi/tarnow/tarnow_switch.py all 1
0 9 * * sun python3 /home/pi/tarnow/tarnow_switch.py all 1
# Monday to Friday at 9:15 am
15 9 * * mon-fri  python3 /home/pi/tarnow/tarnow_switch.py  Radio 0
# Monday to Friday at 6:00 pm
0 18 * * mon-fri python3 /home/pi/tarnow/tarnow_switch.py  Radio 1
# Sunday to Thursday 10:30 am
30 22  * * sun-thu python3 /home/pi/tarnow/tarnow_switch.py  Radio 0
# turn off everyday at midnight
0 0 * * * python3 /home/pi/tarnow/tarnow_switch.py all 0
0 6 * * * python3 /home/pi/tarnow/tarnow_switch.py Nightlight 0
0 22 * * * python3 /home/pi/tarnow/tarnow_switch.py Nightlight 1

0 4 * * * reboot
"""


@pytest.fixture()
def cron():
    yield crontab.CronTab(tab=CRONTAB)


@pytest.fixture()
def now():
    yield datetime(2015, 5, 15, 17, 0, 0)


@pytest.fixture()
def cut(cron, now):
    result = next_execution.NextSwitchExecution('Radio', date=now, crontab=cron)
    yield result
    result.dont_skip_next()
    result.dont_skip_all()

def test_next(cut):
    next_exec = cut.get_next_execution()
    assert next_exec is not None
    (time,status) = next_exec
    assert time == datetime(2015,5,15,18,0,0)
    assert status == 1

def test_next_relative(cut):
    next_exec = cut.get_next_execution()
    assert next_exec is not None
    (time,status) = next_exec

    result_time = cut.get_relative_time()

    assert result_time == "switching on in 1 hour"

def test_next_relative_skip_all(cut):
    cut.skip_all()

    result_time = cut.get_relative_time()

    assert result_time == ""

def test_skip(cut):
    cut.skip_next()
    next_exec = cut.get_next_execution()
    assert next_exec is not None
    (time,status) = next_exec
    assert time == datetime(2015,5,16,0,0,0)
    assert status == 0

def test_next(cut):
    cut.skip_all()
    next_exec = cut.get_next_execution()
    assert next_exec == None

@pytest.mark.skip("The is no configuration nightlight left")
def test_next_dont_use_all_jobs(cut):
    now = datetime(2015,5,15,22,15,0)
    cut=next_execution.NextSwitchExecution('Nightlight', date=now, crontab=cron)
    next_exec = cut.get_next_execution()
    assert next_exec is not None
    (time,status) = next_exec
    assert time == datetime(2015,5,16,6,0,0) # skip the 'all' cronjob on midnight
    assert status == 0