#!/usr/bin/env python3

import os
import subprocess

TEST_FOLDER = "testfiles"
TEST_COMMAND = "./compile.sh {}"

testfiles = [filename for filename in os.listdir(TEST_FOLDER) if
             filename.endswith(".minis")]

for filename in os.listdir(TEST_FOLDER):
    path = os.path.join(TEST_FOLDER, filename)
    final_command = TEST_COMMAND.format(path)
    print("=========")
    print(final_command)
    print("---")
    print(open(path).read().strip())
    print("---")
    subprocess.Popen(final_command.split()).communicate()
    print("=========")
    print("")
