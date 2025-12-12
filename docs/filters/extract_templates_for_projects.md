# 🧩 **Ansible Filter: `extract_templates_for_project`**

The `extract_templates_for_project` filter is a **custom Ansible filter** used in the `semaphoreui_setup` role to generate **dynamic templates** for a specific project.

It takes a set of dynamic template definitions and outputs a **list of fully expanded task templates**, one per inventory, annotated with project and other metadata.

---

## 🔹 **Filter Signature**

```python
extract_templates_for_project(dynamic_template_sets, inventory_list, project_name)
```

### **Parameters**

| Parameter               | Type   | Description                                                          |
| ----------------------- | ------ | -------------------------------------------------------------------- |
| `dynamic_template_sets` | list   | List of dynamic template sets, usually from `dynamic_templates.yml`. |
| `inventory_list`        | list   | List of available inventories for the project.                       |
| `project_name`          | string | The project for which templates should be generated.                 |

---

## 🔹 **Dynamic Template Set Format**

Each entry in `dynamic_template_sets` must contain:

| Key           | Type | Description                                                            |
| ------------- | ---- | ---------------------------------------------------------------------- |
| `project`     | str  | Name of the project this template set belongs to.                      |
| `name_prefix` | str  | Prefix to use when naming the template (e.g., "Check connection to").  |
| `playbook`    | str  | Path to the playbook to run.                                           |
| `inventories` | list | List of inventories the template applies to.                           |
| `view`        | str  | View in Semaphore UI where the template should appear.                 |
| `credentials` | list | List of vault credentials or keys to attach.                           |
| `repository`  | str  | Repository to associate with the template.                             |
| `environment` | str  | Environment to assign. Default: `"Empty"`.                             |
| `app`         | str  | Optional app label for the template. Default: `"ansible"`.             |
| `arguments`   | list | Optional arguments to pass when executing the playbook. Default: `[]`. |

---

## 🔹 **Filter Behavior**

1. Iterates over all dynamic template sets.
2. Filters to only include sets matching the `project_name`.
3. Expands each template across all inventories listed in the template set.
4. Generates a **list of dictionaries** in the following format:

```yaml
- project: "Home Lab"
  name: "Check connection to Plex"
  playbook: "playbooks/linux/check_connection.yml"
  app: "ansible"
  arguments: []
  inventory: "plex"
  credentials:
    - "Ansible vault password"
  repository: "Ansible"
  view: "Linux Checks"
  environment: "Empty"
```

---

## 🔹 **Usage Example in a Playbook or Role**

```yaml
- name: "Generate dynamic templates for a project"
  ansible.builtin.set_fact:
    home_lab_dynamic_templates: >-
      {{ dynamic_template_sets
         | extract_templates_for_project(semaphoreui_setup_inventories, "Home Lab") }}

- name: "Debug generated templates"
  ansible.builtin.debug:
    var: home_lab_dynamic_templates
```

### **Explanation**

1. `dynamic_template_sets` contains all dynamic template definitions.
2. `semaphoreui_setup_inventories` is the list of inventories detected for this project.
3. `"Home Lab"` is the project name for which templates are generated.
4. The filter returns a list of **fully expanded task templates** ready to append to `semaphoreui_setup_projects`.

---

## 🔹 **Integration in Semaphore UI Role**

Dynamic templates are merged into the project definition during setup:

```yaml
- name: "Append dynamic templates to projects"
  ansible.builtin.set_fact:
    semaphoreui_setup_projects: >-
      {{
        semaphoreui_setup_projects
        | map(
            'combine',
            {
              'templates': item.templates + (dynamic_template_sets
                                             | extract_templates_for_project(semaphoreui_setup_inventories, item.name))
            }
          )
        | list
      }}
  loop: "{{ semaphoreui_setup_projects }}"
  loop_control:
    loop_var: item
```

This ensures that **dynamic templates** are fully included alongside **static templates** before Semaphore UI task creation.
