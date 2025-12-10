import sys
from pathlib import Path
import yaml
from collections import defaultdict

def get_playbook_purpose(playbook_path: Path) -> str:
    """Extract mandatory # Purpose comment, supporting multi-line comments after '---'."""
    lines = playbook_path.read_text().splitlines()
    if not lines:
        raise ValueError(f"Playbook {playbook_path} is empty.")

    purpose_lines = []
    found_purpose = False

    for line in lines:
        stripped = line.strip()
        if not stripped:  # skip blank lines
            continue
        if stripped == "---":  # skip YAML doc marker
            continue
        if stripped.startswith("#"):
            text = stripped.lstrip("#").strip()
            if text.lower().startswith("purpose:"):
                found_purpose = True
                purpose_lines.append(text.replace("Purpose:", "").strip())
            elif found_purpose:
                purpose_lines.append(text)
            else:
                continue
        else:
            break

    if not purpose_lines:
        raise ValueError(f"Playbook {playbook_path} is missing a '# Purpose:' comment.")
    return " ".join(purpose_lines)

def get_roles(playbook_path: Path) -> list:
    """Parse roles from the playbook YAML."""
    try:
        data = yaml.safe_load(playbook_path.read_text())
    except Exception as e:
        print(f"Skipping {playbook_path} due to YAML parse error: {e}")
        return []

    roles = []
    if isinstance(data, list):
        for play in data:
            if "roles" in play:
                for role in play["roles"]:
                    if isinstance(role, str):
                        roles.append(role)
                    elif isinstance(role, dict) and "role" in role:
                        roles.append(role["role"])
            if "tasks" in play:
                for task in play["tasks"]:
                    if isinstance(task, dict):
                        if "ansible.builtin.import_role" in task.values():
                            role_name = task.get("ansible.builtin.import_role", {}).get("name")
                            if role_name:
                                roles.append(role_name)
    return roles


def sanitize_purpose(text: str) -> str:
    """Sanitize purpose for safe Markdown table rendering."""
    if not text:
        return ""
    # Collapse newlines into spaces
    sanitized = " ".join(text.splitlines())
    # Escape pipe characters
    sanitized = sanitized.replace("|", "\\|")
    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()
    # Fix malformed Markdown links (ensure [text](url) stays intact)
    sanitized = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"[\1](\2)", sanitized)
    return sanitized

def generate_playbook_markdown(playbook_path: Path, playbooks_dir: Path):
    """Generate README.md content for a playbook."""
    purpose = get_playbook_purpose(playbook_path)
    roles = get_roles(playbook_path)

    rel_path = playbook_path.relative_to(playbooks_dir)

    lines = []
    lines.append(f"# 📖 Playbook: {rel_path}\n")
    lines.append("## 🛠 Purpose")
    lines.append(purpose)

    lines.append("\n## 🔗 Roles Applied")
    if roles:
        for role in roles:
            lines.append(f"- [`{role}`](../roles/{role}/README.md)")
    else:
        lines.append("_No roles detected._")

    lines.append("\n## 🚀 Usage")
    lines.append(f"```bash\nansible-playbook playbooks/{rel_path}\n```")

    return "\n".join(lines), purpose, rel_path

def main():
    playbooks_dir = Path("playbooks")
    index_entries = []
    folder_entries = defaultdict(list)

    # Optional parameter: single playbook path
    if len(sys.argv) > 1:
        playbook_path = Path(sys.argv[1])
        if not playbook_path.exists():
            print(f"Playbook {playbook_path} not found.")
            sys.exit(1)
        markdown, purpose, rel_path = generate_playbook_markdown(playbook_path, playbooks_dir)
        readme_path = playbook_path.with_suffix(".md")
        readme_path.write_text(markdown)
        print(f"Generated README for {playbook_path}")
        return

    # Otherwise, process all playbooks recursively
    for playbook_path in playbooks_dir.rglob("*.yml"):
        try:
            markdown, purpose, rel_path = generate_playbook_markdown(playbook_path, playbooks_dir)
            readme_path = playbook_path.with_suffix(".md")
            readme_path.write_text(markdown)
            index_entries.append({
                "path": rel_path,
                "purpose": purpose
            })
            folder_entries[playbook_path.parent].append({
                "path": playbook_path.name,
                "purpose": purpose
            })
        except ValueError as e:
            print(e)

    # Split root-level vs subfolder playbooks
    root_entries = [e for e in index_entries if len(e["path"].parts) == 1]
    sub_entries = [e for e in index_entries if len(e["path"].parts) > 1]

    # Write global index
    index_lines = ["# 📚 Playbook Index\n"]

    if root_entries:
        index_lines.append("## 📂 Playbooks in root `playbooks/`\n")
        index_lines.append("| Playbook | Purpose |")
        index_lines.append("|----------|---------|")
        for entry in sorted(root_entries, key=lambda x: str(x["path"]).lower()):
            md_path = str(entry["path"]).replace(".yml", ".md")
            purp = sanitize_purpose(entry["purpose"])
            index_lines.append(f"| [`{entry['path']}`]({md_path}) | {entry['purp']} |")

    if sub_entries:
        index_lines.append("\n## 📂 Playbooks in subfolders\n")
        index_lines.append("| Playbook Path | Purpose |")
        index_lines.append("|---------------|---------|")
        for entry in sorted(sub_entries, key=lambda x: str(x["path"]).lower()):
            md_path = str(entry["path"]).replace(".yml", ".md")
            purp = sanitize_purpose(entry["purpose"])
            index_lines.append(f"| [`{entry['path']}`]({md_path}) | {entry['purp']} |")

    (playbooks_dir / "README.md").write_text("\n".join(index_lines))

    # Write folder-level indexes (skip root playbooks/ folder)
    for folder, entries in folder_entries.items():
        if folder == playbooks_dir:
            continue
        rel_folder = folder.relative_to(playbooks_dir)
        lines = [f"# 📚 Playbooks in `{rel_folder}`\n"]
        lines.append("| Playbook | Purpose |")
        lines.append("|----------|---------|")
        for entry in sorted(entries, key=lambda x: x["path"].lower()):
            md_path = entry["path"].replace(".yml", ".md")
            purp = sanitize_purpose(entry["purpose"])
            lines.append(f"| [`{entry['path']}`]({md_path}) | {entry['purp']} |")
        (folder / "README.md").write_text("\n".join(lines))

if __name__ == "__main__":
    main()
