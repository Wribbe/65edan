#!/usr/bin/env python3

import os
import re
import shutil

TEST_FILE = "tests.txt"

class SourceResult:

    def __init__(self, filename):
        self.filename = filename
        self.source = ""
        self.result = ""

def remove_all_tests():

    test_extensions = ['.lang', '.out', '.expected']

    def check_extension(filename):
        for extension in test_extensions:
            if filename.endswith(extension):
                return True
        return False

    for filename in os.listdir('.'):
        if check_extension(filename):
            os.remove(filename)
            continue


def main():

    remove_all_tests()

    with open(TEST_FILE, 'r') as source_handle:
        lines = [line.strip('\n') for line in source_handle.readlines()]

    line_buffer = []
    line_segments = []
    for line in lines:
        if line.startswith('--') and line_buffer:
            line_segments.append(line_buffer)
            line_buffer = []
            line_buffer.append(line)
            continue
        line_buffer.append(line)

    if line_buffer:
        line_segments.append(line_buffer)

    objects = []
    for segment in line_segments:
        ans_part = False
        line_buffer = []
        filename = re.sub('---*\s*', '', segment[0])
        pair_object = SourceResult(filename)
        for line in segment[1:]:
            if line.startswith('=='):
                ans_part = True
                pair_object.source = '\n'.join(line_buffer)
                line_buffer = []
                continue
            line_buffer.append(line)

        if ans_part:
            pair_object.result = '\n'.join(line_buffer)
        else:
            pair_object.source = '\n'.join(line_buffer)

        objects.append(pair_object)

    fmt_expected = "{}.expected"
    fmt_lang = "{}.lang"

    for object in objects:
        filename = object.filename
        with open(fmt_lang.format(filename), 'w') as source_handle:
            with open(fmt_expected.format(filename), 'w') as result_handle:
                source_handle.write(object.source+'\n')
                if not object.result:
                    result_handle.write(object.source+'\n')
                else:
                    result_data = '\n'.join([line for line in
                        object.result.splitlines() if not
                        line.startswith('//')])
                    result_handle.write(result_data+'\n')


if __name__ == "__main__":
    main()
