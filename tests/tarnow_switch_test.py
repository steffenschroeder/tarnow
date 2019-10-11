import unittest
from tarnow import tarnow_switch

from tarnow.switch import Switch
import subprocess


def test_toggle_single():
    tarnow_switch.main(["dontCare", "Radio", 1])
    assert subprocess.call.call_count == 1


def test_toggle_non_existing():
    tarnow_switch.main(["dontCare", "this switch does not exist", 1])
    assert subprocess.call.call_count == 0


def test_wrong_parameter():
    tarnow_switch.main(["dontCare"])
    assert subprocess.call.call_count == 0
    tarnow_switch.main(["dontCare", "Radio"])
    assert subprocess.call.call_count == 0
    tarnow_switch.main(["dontCare", "this switch does not exist", 1, "too much"])
    assert subprocess.call.call_count == 0


def test_toggle_all():
    tarnow_switch.toggle("all", 1)
    assert subprocess.call.call_count == 2


def test_skip_next():
    s = Switch("Radio")
    s.skip_next()
    tarnow_switch.toggle("Radio", 1)
    assert subprocess.call.call_count == 0
    tarnow_switch.toggle("Radio", 1)
    assert subprocess.call.call_count == 1


def test_skip_all():
    s = Switch("Radio")
    s.skip_all()
    tarnow_switch.toggle("Radio", 1)
    assert subprocess.call.call_count == 0
    tarnow_switch.toggle("Radio", 1)
    assert subprocess.call.call_count == 0
    s.dont_skip_all()
    tarnow_switch.toggle("Radio", 1)
    assert subprocess.call.call_count == 1


if __name__ == "__main__":
    unittest.main()
