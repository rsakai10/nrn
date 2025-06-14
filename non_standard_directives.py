import re
import os
import json

def collect_directives_by_file(root):
    pattern = re.compile(r"^.. ([\w:]+)::\s*(.+)?")
    directives_by_file = {}
    for dirpath, _, files in os.walk(root):
        for fname in files:
            if fname.endswith(".rst"):
                fpath = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(fpath, root)
                directives = set()
                with open(fpath, encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        m = pattern.match(line)
                        if m:
                            directive = m.group(1)
                            after = m.group(2) or ""
                            directives.add((directive, after.strip()))
                directives_by_file[rel_path] = directives
    return directives_by_file

if __name__ == "__main__":
    hoc_root = "docs/hoc"
    py_root = "docs/python"
    hoc_directives = collect_directives_by_file(hoc_root)
    py_directives = collect_directives_by_file(py_root)

    result = {}
    all_files = set(hoc_directives) | set(py_directives)
    for rel_path in sorted(all_files):
        hoc_set = hoc_directives.get(rel_path, set())
        py_set = py_directives.get(rel_path, set())
        common = hoc_set & py_set
        hoc_only = hoc_set - py_set
        py_only = py_set - hoc_set

        entry = {}
        if common:
            entry["common"] = [
                {"directive": d, "argument": a} for d, a in sorted(common)
            ]
        if hoc_only:
            entry["hoc_only"] = [
                {"directive": d, "argument": a} for d, a in sorted(hoc_only)
            ]
        if py_only:
            entry["python_only"] = [
                {"directive": d, "argument": a} for d, a in sorted(py_only)
            ]
        if entry:
            result[rel_path] = entry

    with open("directives_comparison.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)