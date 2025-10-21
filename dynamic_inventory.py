#!/usr/bin/env python3

"""
This script dynamically builds all available inventory under the
inventory folder. This can be used to consolidate all the hosts
within a particular group. For example, a dynamic inventory can
be built from hosts that are under the group [python].
"""

import configparser, json, os, sys, re

def get_inventory():
    """
    Walks the inventory folder and reads all *.ini files within
    each inventory.

    args:
        None

    returns:
        a list containing structure that can readily be converted
        as a json document that can be passed to ansible as an
        inventory source.
    """

    inventory = {
        "_meta": {"hostvars": {}},
        "all": {"hosts": []}
    }

    for root, dirs, files in os.walk("inventory"):
        for file in files:
            if file.endswith(".ini"):
                path = os.path.join(root, file)
                parser = configparser.ConfigParser(allow_no_value=True)
                parser.read(path)
                for section in parser.sections():
                    if ':' not in section: # Do not include children sections
                        for host in parser[section]:
                            # Add to 'all' group
                            single_host = re.split(r'\s+', host)[0]
                            if single_host not in inventory["all"]["hosts"]:
                                inventory["all"]["hosts"].append(single_host)
                                # Initialize hostvars
                                inventory["_meta"]["hostvars"].setdefault(single_host, {})

                            # Add to dynamic group based on section name
                            if section not in inventory:
                                inventory[section] = {"hosts": [single_host]}
                            
                            if single_host not in inventory[section]["hosts"]:
                                inventory[section]["hosts"].append(single_host)

    return inventory

def get_host_details(hostname):
    inventory = get_inventory()
    hostvars = inventory["_meta"]["hostvars"]
    return hostvars.get(hostname, {})

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print(json.dumps(get_inventory(), indent=4))
    elif len(sys.argv) == 3 and sys.argv[1] == "--host":
        hostname = sys.argv[2]
        print(json.dumps(get_host_details(hostname), indent=4))
    else:
        print("Usage: {} --list or {} --host <hostname>".format(sys.argv[0], sys.argv[0]))
        sys.exit(1)