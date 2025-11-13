import os
import re
import json

"""
This script defines a custom Ansible filter plugin that consolidates values of the
'pihole_cname_entries' variable from multiple inventory.ini files across an inventory directory.
It aggregates all entries under the specified variable into a single list. This enables
centralized access to cname entry definitions across distributed inventory files.

By default, it searches the 'inventory' folder from the ansible root work folder.

usage: cname_entries: "{{ '' | consolidate_cname_entries }}" 

"""

def consolidate_cname_entries(base_dir="inventory"):
    if not base_dir:
        base_dir = "inventory"

    if not os.path.isdir(base_dir):
        print(f"[WARNING] Inventory base directory '{base_dir}' not found or is not a directory.")
        return []

    consolidated_cname_entries = []

    def scan_inventory(inventory_path):
        inventory_file = os.path.join(inventory_path, "inventory.ini")
        if os.path.isfile(inventory_file):
            with open(inventory_file) as f:
                ini_file = f.readlines()
            # Pattern to match the pihole_cname_entries variable
            pattern = re.compile(r'pihole_cname_entries\s*=\s*\'(.*?)\'')
            # Scan for matches
            for line in ini_file:
                match = pattern.search(line)
                if match:
                    raw_json = match.group(1)
                    try:
                        entries = json.loads(raw_json)
                        consolidated_cname_entries.extend(entries)
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON: {e}")

    # Walk through each inventory folder
    for inventory_name in os.listdir(base_dir):
        inventory_path = os.path.join(base_dir, inventory_name)
        if os.path.isdir(inventory_path):
            scan_inventory(inventory_path)

    return consolidated_cname_entries

class FilterModule(object):
    def filters(self):
        return {
            'consolidate_cname_entries': consolidate_cname_entries
        }

def main():
    consolidated_cname_entries = consolidate_cname_entries()
    print(f"[INFO] Consolidated {len(consolidated_cname_entries)} entries:")
    for entry in consolidated_cname_entries:
        print(f"  {entry['domain']} → {entry['target']}")

if __name__ == "__main__":
    main()
