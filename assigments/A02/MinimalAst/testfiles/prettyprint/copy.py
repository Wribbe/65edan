#!/usr/bin/env python3

import os

for filename in os.listdir('.'):
    if filename.endswith('.lang'):
        name, _ = filename.split('.')
        expected_name = "{}.expected".format(name)
        with open(filename) as source_file:
            with open(expected_name, 'w') as destination_file:
                destination_file.write(source_file.read())
