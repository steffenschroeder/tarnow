import os
import glob
import unittest
from mock import patch

from switch import Switch


class SwitchTest(unittest.TestCase):
    def delete_skip_files(self):
        files = glob.glob('*.skip')
        for f in files:
            os.remove(f)

    def setUp(self):
        self.delete_skip_files()
        self.cut = Switch('Radio')

    def tearDown(self):
        self.delete_skip_files()

    def test_all_skips_are_initially_false(self):
        self.assertFalse(self.cut.is_skip_next())
        self.assertFalse(self.cut.is_skip_all())

    def test_skip_next(self):
        self.cut.skip_next()
        self.assertTrue(self.cut.is_skip_next())
        self.cut.dont_skip_next()
        self.assertFalse(self.cut.is_skip_next())

    def test_skip_permanent(self):
        self.cut.skip_all()
        self.assertTrue(self.cut.is_skip_all())
        self.cut.dont_skip_all()
        self.assertFalse(self.cut.is_skip_all())

    @patch('switch.subprocess.call')
    def test_toggle(self, mock_subprocess):
        self.cut.toggle(1)
        mock_subprocess.assert_called_with(['/usr/local/sbin/send433', '11111', '3', '1'])
        self.cut.toggle(0)
        mock_subprocess.assert_called_with(['/usr/local/sbin/send433', '11111', '3', '0'])

    @patch('switch.subprocess.call')
    def test_toggle_all(self, mock_subprocess):
        Switch.toggle_all(1)
        self.assertEqual(mock_subprocess.call_count, 3)  # 3 switches in the config

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("tarnow.tmp"):
            os.remove("tarnow.tmp")


if __name__ == '__main__':
    unittest.main()
