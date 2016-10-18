#!/usr/bin/env python3

import os
import subprocess
import sys

def main():

    restructure()
    run_compilations()


def restructure():

    for filename in os.listdir('.'):
        if '.expected' in filename:
            name, _ = filename.split('.')
            lines = open(filename, 'r').readlines()
            with open(filename, 'w') as expected_handle:
                with open("{}.input".format(name), 'w') as input_handle:
                    input_handle.write(lines[0])
                expected_handle.write('\n'.join(lines[1:]))


def run_command(tokens):

    print("Running command: {}".format(' '.join(tokens)))
    process = subprocess.Popen(tokens,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out.decode('utf-8'), err.decode('utf-8'), process.returncode


def check(tokens):

    if (returncode != 0):
        print(out)
        print(err)
        sys.exit(0)
    return out


def run_compilations():

    for filename in os.listdir('.'):
        if '.lang' in filename:

            name, _ = filename.split('.')
            executable = "{}.elf".format(name)
            command = "./{}".format(executable).split()

            input_tokens = [elem.strip() for elem in
                    open("{}.input".format(name)).read().split(',')]

            command += input_tokens

            out, err, returncode = run_command(command)
            expected = '\n'.join([line.strip() for line in
                    open("{}.expected".format(name)).readlines() if
                    line.strip()])
            if not returncode == 0:
                out += "!!!! Error: exited with status: {}.".format(returncode)
            if not out.strip() == expected.strip():
                print("!!!! Error: output did not match!")
                print("---- expected:")
                print(expected)
                print("---- received:")
                print(out)
                sys.exit(0)


    print("#### NO ERRORS IN EXECUTION! #####")

if __name__ == "__main__":
    main()
