#!/usr/bin/env python3

import os
import subprocess
import sys

JAR_NAME = "minAstCompiler.jar"

def run(command):
    try:
        command_tokens = command.split(' ')
    except AttributeError: # Is already a list.
        command_tokens = command

    process = subprocess.Popen(command_tokens,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)

    raw_output, raw_error = process.communicate()
    returncode = process.returncode

    # Recode output and error.
    output = raw_output.decode('utf-8')
    error = raw_error.decode('utf-8')

    return output, error, returncode


def indent(text):
    indented_lines = []
    for line in text.splitlines():
        indented_lines.append("  {}".format(line))
    return "\n".join(indented_lines).strip("\n")


def run_in_compiler(filename):

    command = "java -jar {} {}".format(JAR_NAME, filename)

    print("####### {} #######".format(filename))

    with open(filename) as filehandle:
       print("")
       print("contents: ")
       print("")
       print(indent(filehandle.read()))

    output, error, returncode = run(command)

    print("")
    print("Run-output:")
    print("")

    if not output:
        print(indent(error))
    else:
        print(indent(output))
    print("")


def main(args):

    TEST_FOLDER = os.path.join("testfiles", "parser")

    commands = [
        'ant jar',
        'mv compiler.jar {}'.format(JAR_NAME),
    ]

    for command in commands:
        run(command)

    paths_ok = []
    paths_error = []

    for filename in os.listdir(TEST_FOLDER):
        if not filename.endswith(".lang"):
            continue
        file_path = os.path.join(TEST_FOLDER, filename)
        if filename.startswith('error'):
            paths_error.append(file_path)
        else:
            paths_ok.append(file_path)

    testfiles = []
    if not args:
        testfiles = paths_ok
    elif 'err' in args or 'error' in args:
        testfiles = paths_error

    for filepath in testfiles:
        run_in_compiler(filepath)

if __name__ == "__main__":
    main(sys.argv[1:])
