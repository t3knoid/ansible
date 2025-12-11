from ansible.errors import AnsibleFilterError

def extract_templates_for_project(dynamic_template_sets, inventory_list, project_name):
    """
    Generate templates for a specific project.
    Each dynamic template set belongs to a single project.
    Templates are expanded across the inventories listed in the set.
    """
    if not dynamic_template_sets:
        return []
    if not inventory_list:
        return []

    if not isinstance(dynamic_template_sets, list):
        raise AnsibleFilterError("dynamic_template_sets must be a list")
    if not isinstance(inventory_list, list):
        raise AnsibleFilterError("inventory_list must be a list")

    templates = []

    for dt in dynamic_template_sets:
        # Only include template sets for this project
        if dt.get("project") != project_name:
            continue

        for inv in dt.get("inventories", []):
            # Skip inventories not in the list
            if inv not in inventory_list:
                continue

            template = {
                "project": project_name,
                "name": f"{dt.get('name_prefix', 'Template')} {inv}",
                "playbook": dt.get("playbook", ""),
                "app": dt.get("app", "ansible"),
                "arguments": dt.get("arguments", []),
                "inventory": inv,
                "credentials": dt.get("credentials", []),
                "repository": dt.get("repository", "Ansible"),
                "view": dt.get("view", ""),
                "environment": dt.get("environment", "Empty")
            }
            templates.append(template)

    return templates

class FilterModule(object):
    def filters(self):
        return {
            "extract_templates_for_project": extract_templates_for_project
        }
