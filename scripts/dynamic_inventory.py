#!/usr/bin/env python3

"""
This script dynamically builds all available inventory under the
inventory folder and outputs a proper Ansible inventory YAML file.
"""

import configparser, os, re, sys, yaml

def get_inventory():
    """
    Walks the inventory folder and reads all *.ini files within
    each inventory.

    returns:
        dict structured as a proper Ansible inventory
    """
    inventory = {
        "all": {
            "children": {}
        }
    }

    for root, dirs, files in os.walk("inventory"):
        for file in files:
            if file.endswith(".ini"):
                path = os.path.join(root, file)
                parser = configparser.ConfigParser(allow_no_value=True)
                parser.read(path)
                for section in parser.sections():
                    if ':' in section:
                        continue  # skip children sections
                    if section not in inventory["all"]["children"]:
                        inventory["all"]["children"][section] = {"hosts": {}}
                    for host in parser[section]:
                        single_host = re.split(r'\s+', host)[0]
                        # add host to group
                        inventory["all"]["children"][section]["hosts"][single_host] = {}
                        # also ensure host appears under all.hosts
                        if "hosts" not in inventory["all"]:
                            inventory["all"]["hosts"] = {}
                        inventory["all"]["hosts"][single_host] = {}

    return inventory

def get_host_details(hostname):
    inv = get_inventory()
    # hostvars would normally be populated here if you want per-host vars
    return inv["all"]["hosts"].get(hostname, {})

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(yaml.safe_dump(get_inventory(), sort_keys=False))
    elif len(sys.argv) == 3 and sys.argv[1] == "--host":
        hostname = sys.argv[2]
        print(yaml.safe_dump(get_host_details(hostname), sort_keys=False))
    else:
        print(f"Usage: {sys.argv[0]} --list or {sys.argv[0]} --host <hostname>")
        sys.exit(1)
