__author__ = 'mav'

import unittest
import next_execution
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

class MyTestCase(unittest.TestCase):

    def test_next(self):
        next_exec = self.cut.get_next_execution()
        self.assertNotEqual(next_exec,None)
        (time,status) = next_exec
        self.assertEqual(time, datetime(2015,5,15,18,0,0))
        self.assertEqual(status, 1)

    def test_next_relative(self):
        next_exec = self.cut.get_next_execution()
        self.assertNotEqual(next_exec,None)
        (time,status) = next_exec

        result_time = self.cut.get_relative_time()

        self.assertEqual(result_time, "switching on in 1 hour")

    def test_next_relative_skip_all(self):
        self.cut.skip_all()

        result_time = self.cut.get_relative_time()

        self.assertEqual(result_time, "")

    def test_skip(self):
        self.cut.skip_next()
        next_exec = self.cut.get_next_execution()
        self.assertNotEqual(next_exec,None)
        (time,status) = next_exec
        self.assertEqual(time, datetime(2015,5,16,0,0,0))
        self.assertEqual(status, 0)

    def test_next(self):
        self.cut.skip_all()
        next_exec = self.cut.get_next_execution()
        self.assertEqual(next_exec, None)

    def test_next_dont_use_all_jobs(self):
        self.now = datetime(2015,5,15,22,15,0)
        self.cut=next_execution.NextSwitchExecution('Nightlight', date=self.now, crontab=self.cron)
        next_exec = self.cut.get_next_execution()
        self.assertNotEqual(next_exec,None)
        (time,status) = next_exec
        self.assertEqual(time, datetime(2015,5,16,6,0,0)) # skip the 'all' cronjob on midnight
        self.assertEqual(status, 0)

    def setUp(self):
        super(MyTestCase, self).setUp()
        self.cron = crontab.CronTab(tab=CRONTAB)
        self.now = datetime(2015,5,15,17,0,0)
        self.cut=next_execution.NextSwitchExecution('Radio', date=self.now, crontab=self.cron)

    def tearDown(self):
        self.cut.dont_skip_all()
        self.cut.dont_skip_next()


if __name__ == '__main__':
    unittest.main()
