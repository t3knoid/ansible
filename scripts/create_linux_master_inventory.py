"""
Scans all .ini files recursively in the current directory and its subdirectories,
extracts host entries under the [linux] group from each file, and consolidates them
into a single master inventory file named 'master_linux_inventory.ini'.

The resulting file contains a [linux] group header followed by a sorted, deduplicated
list of all hosts found under [linux] groups across the discovered .ini files.

Assumes that host entries are non-empty, non-comment lines under a [linux] section.
"""

import glob
import os
import fnmatch

ini_files = glob.glob('**/*.ini', recursive=True)
linux_hosts = set()
for ini_file in ini_files:
    with open(ini_file, 'r', encoding='utf-8') as f:
        in_linux_group = False
        for line in f:
            stripped = line.strip()
            if stripped.startswith('['):
                in_linux_group = stripped.lower() == '[linux]'
                continue
            if in_linux_group and stripped and not stripped.startswith('#') and not stripped.startswith('[') and stripped != '':
                linux_hosts.add(stripped)

with open('master_linux_inventory.ini', 'w', encoding='utf-8') as master_file:
    master_file.write('[linux]\n')
    for host in sorted(linux_hosts, key=str.lower):
        master_file.write(f'{host}\n')