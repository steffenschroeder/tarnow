import unittest
import tarnow_switch
from unittest.mock import patch
from switch import Switch


class MyTestCase(unittest.TestCase):
    @patch('switch.subprocess.call')
    def test_toggle_all(self, mock_subprocess):
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 1)
    @patch('switch.subprocess.call')
    def test_toggle_all(self, mock_subprocess):
        tarnow_switch.toggle("all", 1)
        self.assertEqual(mock_subprocess.call_count, 3)

    @patch('switch.subprocess.call')
    def test_skip_next(self, mock_subprocess):
        s = Switch("Radio")
        s.skip_next()
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 0)
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 1)

    @patch('switch.subprocess.call')
    def test_skip_all(self, mock_subprocess):
        s = Switch("Radio")
        s.skip_all()
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 0)
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 0)
        s.dont_skip_all()
        tarnow_switch.toggle("Radio", 1)
        self.assertEqual(mock_subprocess.call_count, 1)


if __name__ == '__main__':
    unittest.main()
