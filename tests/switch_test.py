import subprocess
import pytest

from tarnow.switch import Switch


@pytest.fixture()
def cut():
    return Switch("Radio")


def test_all_skips_are_initially_false(cut):
    assert not cut.is_skip_next()
    assert not cut.is_skip_all()


def test_skip_next(cut):
    cut.skip_next()
    assert cut.is_skip_next()
    cut.dont_skip_next()
    assert not cut.is_skip_next()


def test_skip_permanent(cut):
    cut.skip_all()
    assert cut.is_skip_all()
    cut.dont_skip_all()
    assert not cut.is_skip_all()


def test_toggle(cut):
    cut.toggle(1)
    subprocess.call.assert_called_with(["/usr/local/sbin/send433", "11111", "3", "1"])
    cut.toggle(0)
    subprocess.call.assert_called_with(["/usr/local/sbin/send433", "11111", "3", "0"])


def test_toggle_all(cut):
    Switch.toggle_all(1)
    assert subprocess.call.call_count == 2  # 1 switches in the config, one is alwayOn
