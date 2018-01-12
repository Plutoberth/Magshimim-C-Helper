# Created by Cakeofdestiny

import subprocess, sys
from pathlib import Path


def enter_to_exit():
    input("Enter to exit...")
    sys.exit()


def ask_for_file():
    file_name = input("filename: ")
    print("-------------------------------------------------")
    return file_name


def add_headers(func_file_lines, file_name):
    user_input = input("Add headers? Y/N -- ")
    if user_input.lower() != 'y':
        return
    depth = 0
    funcs = []
    last_include = 0
    for line_number, line in enumerate(func_file_lines):
        if line.startswith("#include <"):
            last_include = line_number
        if "{" in line:
            if depth == 0:
                funcs.append(func_file_lines[line_number - 1].replace("\n", ";\n"))
            depth += 1
        if "}" in line:
            depth -= 1

    # we take from the 2nd element of funcs, because int main is the first
    funcs = funcs[1:]

    # I was really lazy, awfully sorry
    # this is basically just to check for double runs of the program, not for anything the user did.
    if func_file_lines[last_include+1:last_include+len(funcs)+1] == funcs:
        print("Signatures already in file. No operation needed.")

    else:
        # We add the function signatures right after the includes
        func_file_lines = func_file_lines[0:last_include+1] + funcs + func_file_lines[last_include+1:]

        with open(file_name, 'w') as file:
            file.writelines(func_file_lines)

        for r in funcs:
            print(r.replace("\n", ""))
        print("-------------------------------------------------")
        print("Successfully written {} function sigantures to {}".format(len(funcs), file_name))


def get_file_data(file_name):
    my_file = Path(file_name)
    if not my_file.is_file():
        print("File not found.")
        enter_to_exit()

    with open(file_name, 'r') as f:
        func_file_lines = f.readlines()
    return func_file_lines


def compile_c(file_name):
    user_input = input("Compile? Y/N -- ")
    if user_input.lower() == 'y':
        proc = subprocess.Popen('gcc -o {0}.exe {0}.c'.format(file_name.replace(".c", "")), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        tmp = proc.stdout.read()
        # Changing to a proper string
        tmp = tmp.decode("utf-8")
        print(tmp)
        num_of_lines = len(tmp.split("\n")) - 1
        if num_of_lines > 0:
            # printing the amount of lines in the response.
            print("Looks like there were some ({}) errors.".format(num_of_lines))
            enter_to_exit()
        else:
            print("Compiled successfully with 0 errors/warnings..")


def run(file_name):
    user_input = input("Run? Y/N -- ")
    if user_input.lower() == 'y':
        print("Running...")
        proc = subprocess.Popen('{}.exe'.format(file_name.replace(".c", "")))
        proc.wait()
        print("\n")


user_file_name = ask_for_file()
file_lines = get_file_data(user_file_name)
add_headers(file_lines, user_file_name)
compile_c(user_file_name)
run(user_file_name)
enter_to_exit()
