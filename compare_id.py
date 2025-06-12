import re
import os
import json


def convert_tabs_to_spaces(text_with_tabs: str, tab_stop: int = 8) -> str:
    """
    Converts tabs in a string to spaces, aligning them to the next multiple of the tab_stop.

    Args:
        text_with_tabs: The input string which may contain tabs.
        tab_stop: The number of spaces a tab represents, and to which columns
                  are aligned (e.g., 8 for standard tab stops).

    Returns:
        A new string with tabs replaced by the appropriate number of spaces.
    """
    if not isinstance(text_with_tabs, str):
        raise TypeError("Input 'text_with_tabs' must be a string.")
    if not isinstance(tab_stop, int) or tab_stop <= 0:
        raise ValueError("Input 'tab_stop' must be a positive integer.")

    converted_text = []
    current_column = 0

    for char in text_with_tabs:
        if char == '\t':
            # Calculate how many spaces are needed to reach the next tab stop
            spaces_needed = tab_stop - (current_column % tab_stop)
            if spaces_needed == 0:
                # If already at a tab stop, a tab still moves to the *next* one
                spaces_needed = tab_stop
            converted_text.append(' ' * spaces_needed)
            current_column += spaces_needed
        elif char == '\n':
            # Reset column count for new line
            converted_text.append(char)
            current_column = 0
        else:
            # Append regular character and increment column count
            converted_text.append(char)
            current_column += 1

    return "".join(converted_text)

def read_lines(filename, tab_stop=8):
    with open(str(filename), encoding="utf-8") as f:
        return [convert_tabs_to_spaces(line.rstrip("\n"), tab_stop) for line in f]


def extract_python_identifiers(py_lines):
    pattern = re.compile(r"\s*\.\. (class|method|data|function)::\s+([A-Za-z0-9_.]+)")
    identifiers = set()
    for line in py_lines:
        match = pattern.match(line)
        if match:
            _, name = match.groups()
            identifiers.add(name)
    return identifiers

def extract_hoc_identifiers(hoc_lines, kinds=None):
    if kinds is None:
        kinds = ["hoc:method", "hoc:data", "hoc:class", "hoc:function"]
    identifiers = set()
    for line in hoc_lines:
        for kind in kinds:
            identifier = f".. {kind}::"
            if identifier in line:
                name = line.split(identifier, 1)[1].strip()
                identifiers.add(name)
    return identifiers


matched_dict = {}
py_only_dict = {}
hoc_only_dict = {}

hoc_root = "has_hoc_directives"
python_root = "docs/python"

for root, _, files in os.walk(hoc_root):
    for fname in files:
        py_path = None
        hoc_path = os.path.join(root, fname)
        # Recursively search for the file in docs/python
        for py_root, _, py_files in os.walk(python_root):
            if fname in py_files:
                py_path = os.path.join(py_root, fname)
                break
        if py_path is not None:
            py_lines = read_lines(py_path)
            hoc_lines = read_lines(hoc_path)
            py_ids = extract_python_identifiers(py_lines)
            hoc_ids = extract_hoc_identifiers(hoc_lines)

            matched = py_ids & hoc_ids
            py_only = py_ids - hoc_ids
            hoc_only = hoc_ids - py_ids

            if matched:
                matched_dict[fname] = {"root": root, "identifiers": list(matched)}
            if py_only:
                py_only_dict[fname] = {"root": root, "identifiers": list(py_only)}
            if hoc_only:
                hoc_only_dict[fname] = {"root": root, "identifiers": list(hoc_only)}


all_identifiers = {
    "matched": matched_dict,
    "python_only": py_only_dict,
    "hoc_only": hoc_only_dict
}

with open("all_identifiers.json", "w", encoding="utf-8") as f:
    json.dump(all_identifiers, f, indent=2)
    print("result saved")