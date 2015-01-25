import os
import fcntl
import subprocess
import sys
import syslog as log

import config


class Switch:
    @classmethod
    def toggle_all(cls, status):
        switches = config.switches
        for switch in switches.keys():
            s = Switch(switch)
            s.toggle(status)

    def __init__(self, name):
        self.name = name
        self.next_skip = Skip(name, 'skip')
        self.all_skip = Skip(name, 'pernament')

    def toggle(self, status):
        lock = Lock()
        try:
            lock.acquire()
            switch_to_change = config.switches.get(self.name)
            if switch_to_change is not None:
                unit_code = str(switch_to_change.get('unitcode'))
                log.syslog("changing status of '%s' to '%s'" % (self.name, status))
                subprocess.call([str(config.executable), str(config.areacode), str(unit_code), str(status)])
            else:
                log.syslog(log.LOG_WARNING, "Called with unknown switch: " + self.name)
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


class Skip:
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
        current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
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