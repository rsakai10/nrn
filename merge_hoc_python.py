import os
import re
import shutil
import pathlib
import subprocess
import sys

def detect_rst_directives(filename):
    hoc_directives = ["hoc:method", "hoc:data", "hoc:class", "hoc:function"]
    found_hoc = False
    with open(filename, encoding="utf-8") as f:
        for line in f:
            for directive in hoc_directives:
                if f".. {directive}::" in line:
                    found_hoc = True
    return found_hoc

def scan_rst_hoc_folder(hoc_dir, hoc_directives_dir):

    for fname in os.listdir(hoc_dir):
        if fname.endswith(".rst"):
            path = os.path.join(hoc_dir, fname)
            found_hoc = detect_rst_directives(path)
            print(f"{fname}:")
            if found_hoc:
                print("contains hoc directives")
                if os.access(hoc_directives_dir, os.W_OK):
                    shutil.copy(path, hoc_directives_dir)
                else:
                    print(f"Error: Directory '{hoc_directives_dir}' is not writable.")

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

def extract_blocks_with_parse_rst_style(lines, kinds=None):
    if kinds is None:
        kinds = ["hoc:method", "hoc:data", "hoc:class", "hoc:function"]
    blocks = []
    i = 0
    while i < len(lines):
        found = False
        for kind in kinds:
            identifier = ".. %s::" % kind
            line = lines[i]
            start = line.find(identifier)
            if start >= 0:
                name = line[start + len(identifier):].strip()
                indent_line = lines[i + 1]
                while not indent_line.strip():
                    i += 1
                    indent_line = lines[i + 1]
                start_indent = len(indent_line) - len(indent_line.lstrip())
                body = []
                while i < len(lines) - 1:
                    i += 1
                    if lines[i].strip():
                        if lines[i].startswith(" " * start_indent):
                            body.append(lines[i][start_indent:])
                        else:
                            break
                    else:
                        if not body or body[-1] != "\n":
                            body.append("\n")
                blocks.append((kind, name, "\n".join(body)))
                found = True
                break
        if not found:
            i += 1
    return blocks

def merge_by_indent(py_lines, hoc_blocks, out_path):
    merged = []
    hoc_dict = {name: (kind, doc) for kind, name, doc in hoc_blocks}
    i = 0
    pattern = re.compile(r"\s*\.\. (class|method|data|function)::\s+([A-Za-z0-9_.]+)")

    while i < len(py_lines):
        line = py_lines[i]
        merged.append(line + "\n")
        match = pattern.match(line)
        if match:
            kind, name = match.groups()
            merged.append("\n    .. tab:: Python\n")
            i += 1
            while i < len(py_lines) and not py_lines[i].strip():
                merged.append("    " + py_lines[i] + "\n")
                i += 1
            indent = len(py_lines[i]) - len(py_lines[i].lstrip()) if i < len(py_lines) else 0
            while i < len(py_lines):
                if py_lines[i].strip() == "":
                    merged.append(py_lines[i] + "\n")
                    i += 1
                    continue
                this_indent = len(py_lines[i]) - len(py_lines[i].lstrip())
                if this_indent >= indent:
                    merged.append("    " + py_lines[i] + "\n")
                    i += 1
                else:
                    break
            if name in hoc_dict:
                _, hoc_doc = hoc_dict[name]
                merged.append("    .. tab:: HOC\n\n\n")
                for hoc_line in hoc_doc.splitlines():
                    merged.append("        " + hoc_line.replace(":hoc:", ":") + "\n")
        else:
            i += 1
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(merged)

# def run_git_command(cmd):
#     try:
#         subprocess.run(cmd, check=True)
#     except subprocess.CalledProcessError:
#         print(f"Git command failed: {' '.join(cmd)}")
#         sys.exit(1)

def git_process(process_dir, branch_name="merge-hoc-python-docs", commit_message="Add generated docs to progref folder"):
    print("\n--- Running Git Commands ---\n")
    # Check if branch exists
    result = subprocess.run(["git", "rev-parse", "--verify", branch_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        subprocess.run(["git", "checkout", branch_name], check=True)
    else:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    subprocess.run(["git", "add", f"docs/progref/{process_dir}"], check=True)
    # Check if there is anything to commit
    diff_result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if diff_result.returncode == 0:
        print("No changes to commit.")
    else:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], check=True)
        print("✅ Push complete.")

if __name__ == "__main__":
    process_dir = "visualization"
    rst_hoc_dir = f"docs/hoc/{process_dir}"
    hoc_directives_dir = "has_hoc_directives" # os.path.join(rst_hoc_dir, "has_hoc_directives")
    py_dir = f"docs/python/{process_dir}"
    out_dir = f"docs/progref/{process_dir}"
    os.makedirs(hoc_directives_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    scan_rst_hoc_folder(rst_hoc_dir, hoc_directives_dir)

    for fname in os.listdir(hoc_directives_dir):
        file = fname[:-4]
        py_path = os.path.join(py_dir, f"{file}.rst")
        hoc_path = os.path.join(hoc_directives_dir, fname)
        out_path = os.path.join(out_dir, f"{file}.rst")
        if os.path.exists(out_path):
            print(f"Skipped (already exists): {file}.rst")
            continue
        if os.path.exists(py_path):
            py_lines = read_lines(py_path)
            hoc_lines = read_lines(hoc_path)
            hoc_blocks = extract_blocks_with_parse_rst_style(hoc_lines)
            merge_by_indent(py_lines, hoc_blocks, out_path)
            print(f"Merged: {file}")
        else:
            print(f"Python file not found for: {file}")

    git_process(process_dir)

