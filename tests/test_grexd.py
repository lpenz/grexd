"""grexd tests"""

import unittest

from grexd import version


class TestGrexdBasic(unittest.TestCase):
    def test_version(self) -> None:
        version()
