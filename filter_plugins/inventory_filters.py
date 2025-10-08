import os

def find_inventory_files(root_path="inventory", filename="inventory.ini"):
    inventory_list = []
    if not os.path.isdir(root_path):
        return inventory_list

    for dirpath, dirnames, filenames in os.walk(root_path):
        if filename in filenames:
            inventory_list.append(os.path.join(dirpath, filename))
    return inventory_list

class FilterModule(object):
    def filters(self):
        return {
            'find_inventory_files': find_inventory_files
        }
