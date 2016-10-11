#!/usr/bin/env python3

import os
import re

TEST_FILE = "tests.txt"

class SourceResult:

    def __init__(self, filename):
        self.filename = filename
        self.source = ""
        self.result = ""

def main():

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
                source_handle.write(object.source)
                if not object.result:
                    result_handle.write(object.source)
                else:
                    result_handle.write(object.result)


if __name__ == "__main__":
    main()
