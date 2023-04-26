import re
import unittest

from framework.types import consts


def parse_url_by_rex(url: str, reg: re.Pattern = consts.DEFAULT_CNFG_URL_PARSER):
    pass


if __name__ == "__main__":

    class ParseUrl(unittest.TestCase):
        def test__parse(self):
            TEST_1 = ("http://main.html", "/main")
            TEST_2 = "http://main/"
            TEST_3 = "/main/<>"

    unittest.main()
