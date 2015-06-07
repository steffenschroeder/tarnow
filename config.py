areacode = "11111"
executable = '/usr/local/sbin/send433'
switches = dict(Radio=dict(unitcode=3),
                Internet=dict(unitcode=2),
                Nightlight=dict(unitcode=4, dontIncludeInAllRuns=True))
BOOTSTRAP_SERVE_LOCAL = True


