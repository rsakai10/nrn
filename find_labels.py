import re
import os
import shutil

def detect_rst_labels(filename):
    label_pattern = re.compile(r"^\s*\.\. _([^\s:]+)(:[^\s:]+)?:\s*$")
    with open(filename, encoding="utf-8") as f:
        for line in f:
            if label_pattern.match(line):
                return True
    return False

def scan_rst_hoc_folder(hoc_dir, hoc_directives_dir):

    for fname in os.listdir(hoc_dir):
        if fname.endswith(".rst"):
            path = os.path.join(hoc_dir, fname)
            found_hoc = detect_rst_labels(path)
            print(f"{fname}:")
            if found_hoc:
                print("contains hoc directives")
                if os.access(hoc_directives_dir, os.W_OK):
                    shutil.copy(path, hoc_directives_dir)
                else:
                    print(f"Error: Directory '{hoc_directives_dir}' is not writable.")


def convert_tabs_to_spaces(text_with_tabs: str, tab_stop: int = 8) -> str:
    converted_text = []
    current_column = 0
    for char in text_with_tabs:
        if char == '\t':
            spaces_needed = tab_stop - (current_column % tab_stop)
            if spaces_needed == 0:
                spaces_needed = tab_stop
            converted_text.append(' ' * spaces_needed)
            current_column += spaces_needed
        elif char == '\n':
            converted_text.append(char)
            current_column = 0
        else:
            converted_text.append(char)
            current_column += 1
    return "".join(converted_text)

def read_lines(filename, tab_stop=8):
    with open(str(filename), encoding="utf-8") as f:
        return [convert_tabs_to_spaces(line.rstrip("\n"), tab_stop) for line in f]



def extract_hoc_blocks_by_label(lines):
    """
    Extract blocks from HOC docs keyed by normalized label (e.g., 'mech_fast' from '_hoc_mech_fast').
    Ignores directives like `.. index::` inside the block content.
    """
    label_pattern = re.compile(r"^\s*\.\. _([^\s:]+):")
    directive_pattern = re.compile(r"^\s*\.\. (class|method|data|function|index|attribute|property)::")
    blocks = {}
    i = 0

    while i < len(lines):
        match = label_pattern.match(lines[i])
        if match:
            full_label = match.group(1)
            label = re.sub(r'^hoc_', '', full_label)

            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1

            block_lines = []
            while i < len(lines):
                next_line = lines[i]
                block_lines.append(next_line)
                i += 1

                # Break after appending if separator is reached
                if next_line.strip() == "----":
                    break
                # Stop if next line is a label or directive
                if i < len(lines):
                    if label_pattern.match(lines[i]) or directive_pattern.match(lines[i]):
                        break

            blocks[label] = "\n".join(block_lines).strip()
        else:
            i += 1

    return blocks


def merge_by_label(py_lines, hoc_blocks, out_path):
    merged = []
    label_pattern = re.compile(r"^\s*\.\. _([^\s:]+):\s*$")
    directive_pattern = re.compile(r"^\s*\.\. (class|method|data|function|index|attribute|property)::\s+(.+)")
    
    i = 0
    while i < len(py_lines):
        line = py_lines[i]
        match = label_pattern.match(line)

        if match:
            label = match.group(1)
            merged.append(line + "\n")
            i += 1

            # Insert Python tab
            merged.append("\n    .. tab:: Python\n\n")

            # Collect and indent Python block
            while i < len(py_lines):
                next_line = py_lines[i]
                if directive_pattern.match(next_line):
                    break
                if label_pattern.match(next_line):
                    break
                if next_line.strip() == "----":
                    i += 1
                    continue
                merged.append("        " + next_line.rstrip() + "\n")
                i += 1

            # Insert HOC block if available
            if label in hoc_blocks:
                merged.append("\n    .. tab:: HOC\n\n")
                for hoc_line in hoc_blocks[label].splitlines():
                    if hoc_line.strip() == "----":
                        continue
                    merged.append("        " + hoc_line.rstrip() + "\n")
            
            if i < len(py_lines):
                next_line = py_lines[i]
                if label_pattern.match(next_line) or directive_pattern.match(next_line):
                    merged.append("----\n\n")

        else:
            merged.append(line + "\n")
            i += 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(merged)

def process_hoc_labels_and_merge(hoc_root, py_roots, out_root):
    """
    For each .rst file in hoc_root with labels, look for the same file in py_roots (in order)
    and merge using extract_hoc_blocks_by_label and merge_by_label.
    """
    os.makedirs(out_root, exist_ok=True)
    for dirpath, _, files in os.walk(hoc_root):
        for fname in files:
            if fname.endswith(".rst"):
                hoc_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(hoc_path, hoc_root)
                hoc_lines = read_lines(hoc_path)
                hoc_blocks = extract_hoc_blocks_by_label(hoc_lines)
                if not hoc_blocks:
                    continue  # Skip files with no labels

                # Try each python root in order
                py_path = None
                for py_root in py_roots:
                    candidate = os.path.join(py_root, rel_path)
                    if os.path.exists(candidate):
                        py_path = candidate
                        break
                if py_path is None:
                    continue  # No matching python/progref file found

                out_path = os.path.join(out_root, rel_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                py_lines = read_lines(py_path)
                merge_by_label(py_lines, hoc_blocks, out_path)
                print(f"Merged: {rel_path}")

# Directory paths
py_root = "docs/progref"
py_fallback = "docs/python"
hoc_root = "docs/hoc"
out_root = "unified_docs_by_label"
os.makedirs(out_root, exist_ok=True)

for dirpath, _, files in os.walk(hoc_root):
    for fname in files:
        if fname.endswith(".rst"):
            hoc_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(hoc_path, hoc_root)

            # Try docs/progref first
            py_path = os.path.join(py_root, rel_path)
            if not os.path.exists(py_path):
                # Fallback to docs/python
                py_path = os.path.join(py_fallback, rel_path)
                if not os.path.exists(py_path):
                    continue  # No matching file found

            out_path = os.path.join(out_root, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            py_lines = read_lines(py_path)
            hoc_lines = read_lines(hoc_path)
            hoc_blocks = extract_hoc_blocks_by_label(hoc_lines)
            merge_by_label(py_lines, hoc_blocks, out_path)
            print(f"Merged: {rel_path}")