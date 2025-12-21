import os
import yaml
from pathlib import Path
import re

def collect_constant_var_files(role_path):
    return [f"{role_path}/vars/main.yml"]

def collect_default_var_files(role_path):
    return [
        f"{role_path}/defaults/main.yml",
        f"{role_path}/defaults/main/main.yml"
    ]

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
            result.append({
                "name": var.strip(),
                "value": val.strip(),
                "comment": current_comment
            })
            current_comment = None
    return result

def load_yaml(file_path):
    if not Path(file_path).exists():
        return {}
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) or {}

def format_vars_table(vars_list, title):
    if not vars_list:
        return f"_No {title.lower()} variables found._"
    lines = ["| Variable | Default Value | Description |",
             "|----------|---------------|-------------|"]
    for var in vars_list:
        comment = var['comment'] if var['comment'] else ""
        lines.append(f"| `{var['name']}` | `{var['value']}` | {sanitize_description(comment)} |")
    return "\n".join(lines)

def sanitize_description(text: str) -> str:
    """Sanitize description for safe Markdown table rendering."""
    if not text:
        return ""
    sanitized = " ".join(text.splitlines())
    sanitized = sanitized.replace("|", "\\|")
    sanitized = sanitized.strip()
    sanitized = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[\1](\2)", sanitized)
    return sanitized

def generate_role_markdown(role_path):
    meta = load_yaml(f"{role_path}/meta/main.yml").get("galaxy_info", {})
    tasks = load_yaml(f"{role_path}/tasks/main.yml")
    handlers = load_yaml(f"{role_path}/handlers/main.yml")
    dependencies = load_yaml(f"{role_path}/meta/main.yml").get("dependencies", [])

    default_vars = []
    for vf in collect_default_var_files(role_path):
        default_vars.extend(extract_vars_with_comments(vf))

    constant_vars = []
    for vf in collect_constant_var_files(role_path):
        constant_vars.extend(extract_vars_with_comments(vf))

    lines = []
    role_name = Path(role_path).name

    lines.append(f"# 🛠️ Role: `{role_name}`\n")

    if meta:
        license_badge = f"![License: {meta.get('license','N/A')}](https://img.shields.io/badge/license-{meta.get('license','N/A')}-blue.svg)"
        ansible_badge = f"![Ansible >= {meta.get('min_ansible_version','N/A')}](https://img.shields.io/badge/ansible-%3E%3D%20{meta.get('min_ansible_version','N/A')}-green.svg)"
        platforms = meta.get("platforms", [])
        platform_names = [p['name'] for p in platforms if 'name' in p]
        platform_badge = f"![Platforms: {' | '.join(platform_names)}](https://img.shields.io/badge/platforms-{'%20|%20'.join(platform_names)}-orange.svg)"
        lines.extend([license_badge, ansible_badge, platform_badge, ""])

    lines.append("## 📖 Overview")
    lines.append(sanitize_description(meta.get("description", "No description provided.")))

    lines.append("\n## 📋 Requirements")
    lines.append(f"- Minimum Ansible version: `{meta.get('min_ansible_version', 'N/A')}`")
    for p in meta.get("platforms", []):
        versions = ', '.join(p.get("versions", [])) if isinstance(p.get("versions", []), list) else ""
        lines.append(f"- Supported on: `{p.get('name','')}` ({versions})")

    lines.append("\n## ⚙️ Defaults")
    lines.append(format_vars_table(default_vars, "default"))

    lines.append("\n## 📦 Vars")
    lines.append(format_vars_table(constant_vars, "constant"))

    lines.append("\n## 📑 Tasks")
    if tasks:
        for task in tasks:
            lines.append(f"- {sanitize_description(task.get('name','Unnamed task'))}")
    else:
        lines.append("_No tasks defined._")

    lines.append("\n## 🔔 Handlers")
    if handlers:
        for handler in handlers:
            lines.append(f"- {sanitize_description(handler.get('name','Unnamed handler'))}")
    else:
        lines.append("_No handlers defined._")

    lines.append("\n## 🔗 Dependencies")
    if dependencies:
        for dep in dependencies:
            dep_name = dep if isinstance(dep, str) else dep.get('role', 'Unknown')
            lines.append(f"- `{sanitize_description(dep_name)}`")
    else:
        lines.append("_No dependencies listed._")

    lines.append("\n## 🚀 Example Usage")
    lines.append(f"```yaml\n- hosts: all\n  roles:\n    - role: {role_name}\n```")

    return '\n'.join(lines), meta.get("description", "No description provided.")

def main():
    roles_dir = Path("roles")
    docs_dir = Path("docs/roles")
    docs_dir.mkdir(parents=True, exist_ok=True)

    index_entries = []

    for role_path in roles_dir.iterdir():
        if not role_path.is_dir():
            continue
        meta_file = role_path / "meta/main.yml"
        if not meta_file.exists():
            continue

        markdown, description = generate_role_markdown(role_path)

        # Write role documentation to docs/roles/<role>.md
        output_path = docs_dir / f"{role_path.name}.md"
        output_path.write_text(markdown)

        index_entries.append({
            "name": role_path.name,
            "description": description
        })

    index_entries.sort(key=lambda x: x["name"].lower())

    index_lines = [
        "# 📚 Role Index\n",
        "| Role | Description |",
        "|------|-------------|"
    ]

    for entry in index_entries:
        desc = sanitize_description(entry["description"])
        index_lines.append(
            f"| [`{entry['name']}`](./{entry['name']}.md) | {desc} |"
        )

    # Write index to docs/roles/README.md
    (docs_dir / "README.md").write_text("\n".join(index_lines))

    # Update roles/README.md with links to docs/roles/
    readme_lines = [
        "# 📚 Roles\n",
        "| Role | Description | Documentation |",
        "|------|-------------|----------------|"
    ]

    for entry in index_entries:
        desc = sanitize_description(entry["description"])
        readme_lines.append(
            f"| `{entry['name']}` | {desc} | [View Documentation](../docs/roles/{entry['name']}.md) |"
        )

    (roles_dir / "README.md").write_text("\n".join(readme_lines))

if __name__ == "__main__":
    main()