#!/usr/bin/env python3

import os
import re

TEST_FILE = "tests.txt"

def main():

    temp_buffer = []
    file_data = {}
    lines = [line.strip('\n') for line in open(TEST_FILE).readlines()]

    filename = ""
    for line in lines:
        if line.startswith('--'):
            if filename: # Don't do the first time.
                file_data[filename] = '\n'.join(temp_buffer)
                temp_buffer = []
            filename = re.sub('--\s*', '', line)
            continue
        else:
            temp_buffer.append(line)


    if temp_buffer:
        file_data[filename] = '\n'.join(temp_buffer)
        temp_buffer = []


    fmt_lang = "{}.lang"
    fmt_expected = "{}.expected"

    for base_name, test_data in file_data.items():
        with open(fmt_lang.format(base_name), 'w') as file_handle:
            file_handle.write(test_data+'\n')
        with open(fmt_expected.format(base_name), 'w') as file_handle:
            file_handle.write(test_data+'\n')

if __name__ == "__main__":
    main()
