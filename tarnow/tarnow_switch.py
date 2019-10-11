import sys
import syslog

from tarnow import Switch


def toggle(switch_name, status):
    switch = Switch(switch_name)
    switch.toggle(status)


def main(args=sys.argv):
    if len(args) != 3:
        syslog.syslog(syslog.LOG_ERR, "Wrong number of arguments: expected: 2 , got %d" % (len(args) - 1))
        return
    switch_name, status = args[1:]
    toggle(switch_name, status)


if __name__ == '__main__':
    main()

