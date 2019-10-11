from .switch import Switch
from datetime import datetime
from croniter import croniter
from crontab import CronTab


class NextSwitchExecution(Switch):
    def __init__(self, name, date=None, crontab=None):
        super(NextSwitchExecution, self).__init__(name)
        self.crontab = crontab or CronTab()
        self.date = date or datetime.today()

    def get_next_execution(self):
        if self.is_skip_all():
            return None
        jobs = self._get_relevant_jobs()

        if not jobs:
            return

        jobs.sort(key=lambda x: x["nextExecution"])

        if self.is_skip_next():
            next_execution_of_relevant_jobs = jobs[1]
        else:
            next_execution_of_relevant_jobs = jobs[0]
        return (
            next_execution_of_relevant_jobs["nextExecution"],
            int(next_execution_of_relevant_jobs["command"][-1]),
        )

    def _get_relevant_jobs(self):
        jobs = []
        for job in self.crontab:
            slices = str(job.slices.clean_render())

            if "tarnow" not in job.command:
                continue

            if self.name in job.command or (
                "all" in job.command and not self.dontIncludeInAllRuns
            ):
                my_iter = croniter(slices, self.date)
                nextExec = my_iter.get_next(datetime)
                jobs.append(
                    dict(slice=slices, nextExecution=nextExec, command=job.command)
                )

        return jobs

    def get_relative_time(self):
        a = self.get_next_execution()
        if a:
            return "switching %s in %s" % (
                ("on" if a[1] else "off"),
                get_age(self.date, a[0]) if a else "",
            )
        else:
            return ""


# Inspired by https://gist.github.com/zhangsen/1199964
def get_age(date1, date2):
    """Take a datetime and return its "age" as a string.

    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.

    Make sure date is not in the future, or else it won't work.
    """

    def formatn(n, s):
        """Add "s" if it's plural"""

        if n == 1:
            return "1 %s" % s
        elif n > 1:
            return "%d %ss" % (n, s)

    def q_n_r(a, b):
        """Return quotient and remaining"""

        return a / b, a % b

    class PrettyDelta:
        def __init__(self, dt, now=None):
            now = now or datetime.now()
            delta = now - dt
            self.day = delta.days
            self.second = delta.seconds

            self.year, self.day = q_n_r(self.day, 365)
            self.month, self.day = q_n_r(self.day, 30)
            self.hour, self.second = q_n_r(self.second, 3600)
            self.minute, self.second = q_n_r(self.second, 60)

        def format(self):
            for period in ["year", "month", "day", "hour", "minute", "second"]:
                n = getattr(self, period)
                if n > 0:
                    return formatn(n, period)
            return "0 second"

    return PrettyDelta(date1, date2).format()
