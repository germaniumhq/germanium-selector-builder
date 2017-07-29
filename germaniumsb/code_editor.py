
import re


def extract_code(full_text, cursor_position):
    lines = str(full_text).split("\n")

    no_spaces = re.compile(r"^[^\s].*$")

    result = []

    for i in reversed(range(cursor_position['row'] + 1)):
        result.insert(0, lines[i])

        if no_spaces.match(lines[i]):
            break

    for i in range(cursor_position['row'] + 1, len(lines)):
        if no_spaces.match(lines[i]):
            break

        result.append(lines[i])

    return str.join("\n", result)


def insert_code_into_editor(cursor, text):
    cursor.beginEditBlock()
    cursor.insertText(text)
    cursor.endEditBlock()
