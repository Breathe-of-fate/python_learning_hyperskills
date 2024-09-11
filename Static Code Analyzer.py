import os, sys, re, ast

def length(file, ind, line):
    if len(line) > 79:
        print(f"{file}: Line {ind + 1}: S001 Too long")

def identation(file, ind, line):
    if (len(line) - len(line.lstrip())) % 4:
        print(f"{file}: Line {ind + 1}: S002 Indentation is not a multiple of four")

def semicolumn(file, ind, line):
    if ";" in line:
        code = line.split("#")[0].strip()
        if code.endswith(";"):
            print(f"{file}: Line {ind + 1}: S003 Unnecessary semicolon")

def comment(file, ind, line):
    if "#" in line:
        position = line.find("#")
        if position != 0 and "  " not in line[position - 2:position]:
                print(f"{file}: Line {ind + 1}: S004 At least two spaces required before inline comments")

def todo(file, ind, line):
    if "todo" in line.lower() and "#" in line:
        if line.lower().find("todo") > line.find("#"):
            print(f"{file}: Line {ind + 1}: S005 TODO found")

def empty_lines(file, ind, lines):
    if ind >= 2:
        if all([len(lines[ind - 1].strip("\n")) == 0,
                len(lines[ind - 2].strip("\n")) == 0,
                len(lines[ind - 3].strip("\n")) == 0]):
            print(f"{file}: Line {ind + 1}: S006 More than two blank lines used before this line")

def def_class(file, ind, line):
    if found := re.match(r" *(def|class)( +)(\w+)", line):
        def_class = found.group(1)
        spaces = found.group(2)
        name = found.group(3)
        if len(spaces) > 1:
            print(f"{file}: Line {ind + 1}: S007 Too many spaces after '{def_class}'")
        if def_class == "class" and not re.match(r"^(?:[A-Z][a-z]+)+$", name):
            print(f"{file}: Line {ind + 1}: S008 Class name '{name}' should use CamelCase")
        if def_class == "def" and not re.match(r"^[a-z_\d]+", name):
            print(f"{file}: Line {ind + 1}: S009 Function name '{name}' should use snake_case")

def argument_name(file, ind, code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and hasattr(node, 'lineno') and node.lineno == ind:
            for arg in node.args.args:
                if not re.match(r'^[a-z_\d]+$', arg.arg):
                    print(f"{file}: Line {ind}: S010 Argument name '{arg.arg}' should be snake_case")

def variable_name(file, ind, code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and hasattr(node, 'lineno') and node.lineno == ind:
            if not re.match(r'^[a-z_\d]+$', node.id):
                print(f"{file}: Line {ind}: S011 Variable '{node.id}' in function should be snake_case")

def argument_type(file, ind, code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and hasattr(node, 'lineno') and node.lineno == ind:
            for item in node.args.defaults:
                if isinstance(item, ast.List):
                    print(f"{file}: Line {ind}: S012 Default argument value is mutable")

def open_n_check(file_name):
    with open(file_name, "r") as file:
        contents = file.readlines()
        full_code = "".join(contents)
    for row_num, content in enumerate(contents):
        content = content.strip("\n")
        length(file_name, row_num, content)
        identation(file_name, row_num, content)
        semicolumn(file_name, row_num, content)
        comment(file_name, row_num, content)
        todo(file_name, row_num, content)
        empty_lines(file_name, row_num, contents)
        def_class(file_name, row_num, content)
        argument_name(file_name, row_num, full_code)
        variable_name(file_name, row_num, full_code)
        argument_type(file_name, row_num, full_code)

def find_files():
    user_input = sys.argv[1]
    path_to_files = []
    if os.path.isfile(user_input):
        path_to_files.append(user_input)
    else:
        for dirpath, dirnames, filenames in os.walk(user_input):
            for filename in filenames:
                path_to_files.append(os.path.join(dirpath, filename))
    return path_to_files

for file in find_files():
    open_n_check(file)