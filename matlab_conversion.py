import os
import re
import openai

# Create OpenAI client with organization
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization="org-3z6NAgNdNa6W5HskVBdfqbxJ"
)

def extract_code_block_lines(lines, start_index):
    """Extracts an indented code block starting at start_index."""
    code_lines = []
    code_block_indent = None
    index = start_index

    while index < len(lines):
        line = lines[index]
        if code_block_indent is None:
            if line.strip() == '':
                index += 1
                continue
            code_block_indent = len(line) - len(line.lstrip())

        if line.strip() == '' or (len(line) - len(line.lstrip()) >= code_block_indent):
            code_lines.append(line[code_block_indent:] if line.strip() else '')
            index += 1
        else:
            break

    return code_lines, index

def extract_python_codeblocks(rst_path):
    with open(rst_path, encoding='utf-8') as f:
        lines = f.readlines()

    code_blocks = []
    codeblock_pattern = re.compile(r'\s*\.\. (code-block|code)::\s*(python)?\s*$')
    i = 0

    while i < len(lines):
        if codeblock_pattern.match(lines[i]):
            i += 1
            code_lines, i = extract_code_block_lines(lines, i)
            if code_lines:
                code_blocks.append('\n'.join(code_lines))
        else:
            i += 1

    return code_blocks

def gpt_python_to_matlab(py_code):
    prompt = (
        "Assume there is a matlab interface in NEURON and convert the following Python code to MATLAB code. "
        "from neuron import n, gui should be converted to n = neuron.launch(); Only output the MATLAB code. Do not add any mark-down style backticks (e.g., ```matlab)\n\n"
        f"Python code:\n{py_code}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in MATLAB and Python."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def convert_rst_python_blocks_to_matlab(rst_path, out_path):
    with open(rst_path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    codeblock_pattern = re.compile(r'\s*\.\. (code-block|code)::\s*(python)?\s*$')
    inline_code_pattern = re.compile(r'``([^`]+)``')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Handle Syntax: blocks with grouped inline Python code
        if line.strip().startswith('Syntax:'):
            new_lines.append(line)
            i += 1
            collected_code = []
            while i < len(lines):
                subline = lines[i]
                if subline.strip().startswith('Description:'):
                    break  # End of syntax block
                matches = inline_code_pattern.findall(subline)
                collected_code.extend(matches)
                i += 1  # only increment here

            if collected_code:
                indent = len(line) - len(line.lstrip()) + 4
                new_lines.append('\n' + ' ' * indent + '.. code-block:: matlab\n\n')
                for code in collected_code:
                    matlab_code = gpt_python_to_matlab(code)
                    for ml in matlab_code.splitlines():
                        if ml.strip():
                            new_lines.append(' ' * (indent + 4) + ml + '\n')
                new_lines.append('\n')

            # Skip i += 1 below — already incremented during Syntax: handling
            continue

        else:
            new_lines.append(line)
            i += 1  # only increment here for non-Syntax lines

    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
def find_python_codeblocks(root_dir):
    pattern = re.compile(r'\s*\.\. code-block::\s*(python)?\s*$')
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.rst'):
                fpath = os.path.join(dirpath, fname)
                with open(fpath, encoding='utf-8') as f:
                    for idx, line in enumerate(f, 1):
                        if pattern.match(line):
                            print(f"{fpath}:{idx}: {line.strip()}")

def batch_convert_rst_python_blocks_to_matlab(src_root, dst_root):
    for dirpath, _, filenames in os.walk(src_root):
        for fname in filenames:
            if fname.endswith('.rst'):
                src_path = os.path.join(dirpath, fname)
                # Mirror directory structure in dst_root
                rel_path = os.path.relpath(src_path, src_root)
                dst_path = os.path.join(dst_root, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                print(f"Converting: {src_path} -> {dst_path}")
                convert_rst_python_blocks_to_matlab(src_path, dst_path)

# Example usage:
# This will convert all .rst files under docs/python to docs/matlab
#batch_convert_rst_python_blocks_to_matlab('docs/python', 'docs/matlab')

convert_rst_python_blocks_to_matlab("docs/python/visualization/graph.rst", "docs/matlab/visualization/graph.rst")