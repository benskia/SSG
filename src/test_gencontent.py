import unittest

from gencontent import extract_title


class TestGeneratePage(unittest.TestCase):
    # extract_title()
    def test_title(self):
        result = extract_title("# Title")
        expect = "Title"
        self.assertEqual(result, expect)

    def test_title_missing(self):
        md = "## Sub-heading\n\nSome `code` here"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_title_order(self):
        md = "## Sub-heading\n\n# Title"
        with self.assertRaises(Exception):
            extract_title(md)
