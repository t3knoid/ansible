import os
import yaml

def load_yaml_file(path):
    if not os.path.isfile(path):
        return {}
    with open(path, 'r') as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError:
            return {}

def consolidate_rproxy_setup_sites(base_dir="inventory", target_var="rproxy_setup_sites"):
    consolidated_sites = []

    def scan_inventory(inventory_path):
        # Check group_vars/all/main.yml explicitly
        all_main = os.path.join(inventory_path, "group_vars", "all", "main.yml")
        if os.path.isfile(all_main):
            data = load_yaml_file(all_main)
            if target_var in data:
                consolidated_sites.extend(data[target_var])

        # Scan group_vars and host_vars
        for subdir in ["group_vars", "host_vars"]:
            sub_path = os.path.join(inventory_path, subdir)
            if not os.path.isdir(sub_path):
                continue
            for filename in os.listdir(sub_path):
                full_path = os.path.join(sub_path, filename)
                if full_path == all_main:
                    continue
                if filename.endswith(".yml") or filename.endswith(".yaml"):
                    data = load_yaml_file(full_path)
                    if target_var in data:
                        consolidated_sites.extend(data[target_var])

    # Walk through each inventory folder
    for inventory_name in os.listdir(base_dir):
        inventory_path = os.path.join(base_dir, inventory_name)
        if os.path.isdir(inventory_path):
            scan_inventory(inventory_path)

    return consolidated_sites

class FilterModule(object):
    def filters(self):
        return {
            'consolidate_rproxy_setup_sites': consolidate_rproxy_setup_sites
        }
    