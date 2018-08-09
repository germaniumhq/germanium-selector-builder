from typing import Dict

import unittest

from germaniumsb.code_editor import extract_code


def cursor(row: int, col: int) -> Dict[str, int]:
    return {'row': row, 'col': col}


EDITOR_CODE = """XPath('a')

XPath('input')
XPath('a',
      exact_text="wut")
XPath('input')
"""


class TestCodeEditor(unittest.TestCase):
    """
    Tests the extraction of the code from the live editor.
    """
    def test_code_extraction(self):
        """
        Test simple code extraction on a single line.
        """
        self.assertEqual("XPath('a')", extract_code(EDITOR_CODE, cursor(0, 1)))
        self.assertEqual("", extract_code(EDITOR_CODE, cursor(1, 1)))
        self.assertEqual("XPath('input')", extract_code(EDITOR_CODE, cursor(2, 1)))
        self.assertEqual('XPath(\'a\',\n      exact_text="wut")', extract_code(EDITOR_CODE, cursor(3, 1)))
        self.assertEqual('XPath(\'a\',\n      exact_text="wut")', extract_code(EDITOR_CODE, cursor(4, 1)))
        self.assertEqual("XPath('input')", extract_code(EDITOR_CODE, cursor(5, 1)))


if __name__ == '__main__':
    unittest.main()
