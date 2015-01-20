import sys
import syslog

from switch import Switch
import config


def main():
    if len(sys.argv) != 3:
        syslog.syslog(syslog.LOG_ERR, "Wrong number of arguments: expected: 2 , got %d" % (len(sys.argv) - 1))
        exit(1)

    switch_name, status = sys.argv[1:]

    if switch_name not in config.switches and switch_name != "all":
        syslog.syslog(syslog.LOG_WARNING, "no configuration found for switch '%s'. Will exit" % switch_name)
        sys.exit(1)

    switch = Switch(switch_name)
    if switch.is_skip_all():
        syslog.syslog("Skipping permanently " + switch.name)
    elif switch.is_skip_next():
        syslog.syslog("Skipping " + switch.name)
        # delete the file
        switch.dont_skip_next()
    else:
        switch.toggle(status)




if __name__ == '__main__':
    main()

