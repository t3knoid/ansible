import os
import yaml
from pathlib import Path

def collect_constant_var_files(role_path):
    constant_var_files = []

    constant_var_files += [f"{role_path}/vars/main.yml"]

    return constant_var_files

def collect_default_var_files(role_path):
    default_var_files = []

    # defaults
    default_var_files += [
        f"{role_path}/defaults/main.yml",
        f"{role_path}/defaults/main/main.yml"
    ]
    return default_var_files

def extract_vars_with_comments(file_path):
    if not Path(file_path).exists():
        return []

    lines = Path(file_path).read_text().splitlines()
    result = []
    current_comment = None

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            current_comment = line.lstrip("#").strip()
        elif ":" in line:
            var, val = line.split(":", 1)
            var = var.strip()
            val = val.strip()
            result.append({
                "name": var,
                "value": val,
                "comment": current_comment
            })
            current_comment = None
    return result

def load_yaml(file_path):
    if not Path(file_path).exists():
        return {}
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) or {}

def generate_role_markdown(role_path):
    meta = load_yaml(f"{role_path}/meta/main.yml").get("galaxy_info", {})
    vars_ = load_yaml(f"{role_path}/vars/main.yml")
    tasks = load_yaml(f"{role_path}/tasks/main.yml")

    lines = []

    # Title
    lines.append(f"# Role: `{Path(role_path).name}`\n")

    # Overview
    lines.append("## 📖 Overview")
    lines.append(meta.get("description", "No description provided."))

    # Requirements
    lines.append("\n## 📋 Requirements")
    lines.append(f"- Minimum Ansible version: `{meta.get('min_ansible_version', 'N/A')}`")
    platforms = meta.get("platforms", [])
    for p in platforms:
        versions = ', '.join(p.get("versions", []))
        lines.append(f"- Supported on: `{p['name']}` ({versions})")

    # Defaults
    lines.append("\n## 🧮 Defaults")
    default_var_files = collect_default_var_files(role_path)
    all_default_vars = []

    for vf in default_var_files:
        all_default_vars.extend(extract_vars_with_comments(vf))

    if all_default_vars:
        for var in all_default_vars:
            comment = f" — {var['comment']}" if var['comment'] else ""
            lines.append(f"- `{var['name']}`: `{var['value']}`{comment}")
    else:
        lines.append("_No default variables found in defaults._")

    # Constants
    lines.append("\n## 🧮 Vars")
    constant_var_files = collect_constant_var_files(role_path)
    all_constant_vars = []

    for vf in constant_var_files:
        all_constant_vars.extend(extract_vars_with_comments(vf))

    if all_constant_vars:
        for var in all_constant_vars:
            comment = f" — {var['comment']}" if var['comment'] else ""
            lines.append(f"- `{var['name']}`: `{var['value']}`{comment}")
    else:
        lines.append("_No constant variables found in vars._")

    # Tasks
    lines.append("\n## 🛠 Tasks")
    if tasks:
        for task in tasks:
            name = task.get("name", "Unnamed task")
            lines.append(f"- {name}")
    else:
        lines.append("_No tasks defined._")

    # Example
    lines.append("\n## 🚀 Example Usage")
    lines.append("```yaml\n- hosts: all\n  roles:\n    - role: " + Path(role_path).name + "\n```")

    return '\n'.join(lines), meta.get("description", "No description provided.")

def main():
    roles_dir = Path("roles")
    index_entries = []

    for role_path in roles_dir.iterdir():
        if not role_path.is_dir():
            continue
        meta_file = role_path / "meta/main.yml"
        if not meta_file.exists():
            continue

        markdown, description = generate_role_markdown(role_path)
        readme_path = role_path / "README.md"
        readme_path.write_text(markdown)

        index_entries.append({
            "name": role_path.name,
            "description": description
        })

    # Sort alphabetically by role name
    index_entries.sort(key=lambda x: x["name"].lower())

    # Write index
    index_lines = ["# 📚 Role Index\n"]
    for entry in index_entries:
        index_lines.append(f"- [`{entry['name']}`]({entry['name']}/README.md): {entry['description']}")

    index_path = roles_dir / "README.md"
    index_path.write_text('\n'.join(index_lines))

if __name__ == "__main__":
    main()
