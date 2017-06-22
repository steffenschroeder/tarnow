import os
import fcntl
import subprocess
import sys
import syslog as log

import config


class Switch(object):
    def __str__(self):
        return "Name: '%s', NextSkip: '%s', AllSkip: '%s'" % (self.name, str(self.next_skip), str(self.all_skip))

    @classmethod
    def toggle_all(cls, status):
        switches = config.switches
        for switch in switches.keys():
            s = Switch(switch)
            if not s.dontIncludeInAllRuns:
                s.toggle(status)

    def __init__(self, name, all_switches=config.switches):
        self.name = name
        self.next_skip = Skip(name, 'skip')
        self.all_skip = Skip(name, 'pernament')
        self.all_switches = all_switches
        self._initAlwaysOn()

    def toggle(self, status):
        if self.is_skip_all():
            log.syslog("Skipping permanently " + self.name)
            return
        elif self.is_skip_next():
            log.syslog("Skipping " + self.name)
            # delete the file
            self.dont_skip_next()
            return

        if self.name in config.switches:
            self._change_status(status)
        elif self.name == "all":
            Switch.toggle_all(status)
        else:
            log.syslog(log.LOG_WARNING, "Called with unknown switch: " + self.name)

    def _change_status(self, status):
        lock = Lock()
        try:
            lock.acquire()
            switch_to_change = self.all_switches.get(self.name)
            unit_code = str(switch_to_change.get('unitcode'))
            log.syslog("changing status of '%s' to '%s'" % (self.name, status))
            subprocess.call([str(config.executable), str(config.areacode), str(unit_code), str(status)])
        finally:
            lock.release()

    def is_skip_next(self):
        return self.next_skip.enabled()

    def is_skip_all(self):
        return self.all_skip.enabled()

    def dont_skip_next(self):
        self.next_skip.delete()

    def dont_skip_all(self):
        self.all_skip.delete()

    def skip_next(self):
        self.next_skip.create()

    def skip_all(self):
        self.all_skip.create()

    def _initAlwaysOn(self):
        self.dontIncludeInAllRuns = False
        if self.name in self.all_switches.keys():
            s = self.all_switches.get(self.name)
            self.dontIncludeInAllRuns = s.get('dontIncludeInAllRuns',False)


class Skip(object):
    def __str__(self):
        return "Name: '%s', Type: '%s', enabled: ''%s" % (self.name,self.type, self.enabled())

    def __init__(self, name, skiptype):
        self.name = name
        self.type = skiptype
        self._generate_file_name()

    def enabled(self):
        return os.path.exists(self.skipfilename)

    def create(self):
        with open(self.skipfilename, 'a'):
            os.utime(self.skipfilename, None)

    def delete(self):
        if os.path.exists(self.skipfilename):
            os.remove(self.skipfilename)

    def _generate_file_name(self):
        home = os.path.expanduser("~")
        current_path = home + os.sep + '.tarnow'
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        self.skipfilename = current_path + os.sep + self.type + self.name + ".skip"


# Inspired by: http://blog.vmfarms.com/2011/03/cross-process-locking-and.html """
class Lock:
    def __init__(self, filename="tarnow.tmp"):
        self.filename = filename
        self.handle = open(filename, 'w')

    def acquire(self):
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        self.handle.close()