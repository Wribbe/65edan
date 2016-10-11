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

    if not returncode == 0: # Run failed.
        print(output)
        print(error)
        raise RunException

    return output, error, returncode

class RunException(Exception):
    pass


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

    errors = 0
    for command in commands:
        try:
            run(command)
        except RunException:
            errors += 1

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
    if 'err' in args or 'error' in args:
        testfiles = paths_error
    else:
        testfiles = paths_ok

    for filepath in testfiles:
        try:
            run_in_compiler(filepath)
        except RunException:
            errors += 1

    print("#####")
    if errors:
        format_string = "##### Result: {0} errors ({0}/{1} error-files). ######"
        print(format_string.format(errors, len(paths_error)))
    else:
        print("##### Result: NO ERRORS. ######")
    print("#####")

if __name__ == "__main__":
    main(sys.argv[1:])
