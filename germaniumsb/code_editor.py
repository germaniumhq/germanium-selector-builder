from typing import Dict, List
import re


def extract_code(full_text: str, cursor_position: Dict[str, int]) -> str:
    lines = str(full_text).split("\n")

    if not lines[cursor_position['row']]:
        return ""

    no_spaces = re.compile(r"^[^\s].*$")

    result: List[str] = []

    for i in reversed(range(cursor_position['row'] + 1)):
        result.insert(0, lines[i])

        if no_spaces.match(lines[i]):
            break

    for i in range(cursor_position['row'] + 1, len(lines)):
        if no_spaces.match(lines[i]):
            break

        result.append(lines[i])

    return str.join("\n", result).strip()


def insert_code_into_editor(cursor, text: str) -> None:
    cursor.beginEditBlock()
    cursor.insertText(text)
    cursor.endEditBlock()
