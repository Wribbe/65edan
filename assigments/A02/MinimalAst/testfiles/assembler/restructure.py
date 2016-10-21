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


def run_command(tokens, input_list):

    message = "Running command: {}".format(' '.join(tokens))
    if "no input" in " ".join(input_list).lower():
        input_list = []
    if input_list:
        input_string = "\r".join(input_list)+"\r";
        message += " {}".format(' '.join(input_list))

    print(message)

    process = subprocess.Popen(tokens,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)

    import time
    for input_token in input_list:
        process.stdin.write(bytes(input_token+'\n', 'utf-8'));
        process.stdin.flush()
        time.sleep(1);
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
                    open("{}.input".format(name)).read().split(' ')]

            out, err, returncode = run_command(command, input_tokens)
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
