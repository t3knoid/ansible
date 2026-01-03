#!/usr/bin/env python3
import sys
import shlex
from pathlib import Path
from collections import defaultdict
import argparse
import os
import logging
import shutil

# ------------------------------
# Global Structures
# ------------------------------
HOST_INDEX = defaultdict(lambda: {"inventories": set(), "groups": set()})
INVENTORY_META = {}

# ------------------------------
# Inventory Parsing
# ------------------------------
def parse_ini_inventory(inv_path: Path):
    """
    Parse an INI-style Ansible inventory file.

    Returns:
        groups: dict[group_name] = set(hosts)
        host_vars: dict[host] = dict(var_name: value)
        group_vars: dict[group_name] = dict(var_name: value)
        group_children: dict[group_name] = set(child_groups)
    """
    groups = defaultdict(set)
    host_vars = defaultdict(dict)
    group_vars = defaultdict(dict)
    group_children = defaultdict(set)

    current_group = None
    current_section_type = None  # 'hosts', 'vars', 'children'

    # Determine inventory name for host index
    inventory_name = inv_path.parent.name if inv_path.parent.name != "inventory" else inv_path.stem

    for line in inv_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Section headers
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1].strip()
            if section.endswith(':vars'):
                current_group = section[:-5]
                current_section_type = 'vars'
            elif section.endswith(':children'):
                current_group = section[:-9]
                current_section_type = 'children'
            else:
                current_group = section
                current_section_type = 'hosts'
            continue

        # Parse based on section type
        if current_section_type == 'hosts':
            parts = shlex.split(line)
            if not parts:
                continue
            hostname = parts[0]
            groups[current_group].add(hostname)
            if len(parts) > 1:
                # Inline host variables
                for assignment in parts[1:]:
                    if '=' in assignment:
                        var, val = assignment.split('=', 1)
                        host_vars[hostname][var] = val
            # Update global host index
            HOST_INDEX[hostname]["inventories"].add(inventory_name)
            HOST_INDEX[hostname]["groups"].add(current_group)
        elif current_section_type == 'vars':
            if '=' in line:
                var, val = line.split('=', 1)
                group_vars[current_group][var.strip()] = val.strip()
        elif current_section_type == 'children':
            group_children[current_group].add(line.strip())
        else:
            logging.warning(f"Unknown section type at line: {line}")

    return groups, host_vars, group_vars, group_children

# ------------------------------
# Duplicate Host Detection
# ------------------------------
def report_duplicate_hosts(strict=False):
    duplicates = {h: info for h, info in HOST_INDEX.items() if len(info["inventories"]) > 1}
    for host, info in duplicates.items():
        logging.warning(f"Duplicate host detected: {host} in inventories: {', '.join(info['inventories'])}")
    if strict and duplicates:
        raise RuntimeError("Duplicate hosts found and strict mode is enabled.")

# ------------------------------
# Generate Per-Inventory Doc
# ------------------------------
def generate_inventory_doc(inv_path: Path, docs_dir: Path):
    inventory_name = inv_path.parent.name if inv_path.parent.name != "inventory" else inv_path.stem
    groups, host_vars, group_vars, group_children = parse_ini_inventory(inv_path)

    # Build markdown
    lines = [f"# 🗂 Inventory: `{inventory_name}`\n"]
    lines.append(f"_Inventory for `{inventory_name}` hosts_\n")
    lines.append(f"📄 **Source:** [`{inv_path}`](../../{inv_path})\n")

    lines.append("## 👥 Groups & Hosts")
    for group, hosts in groups.items():
        lines.append(f"### `{group}`")
        if hosts:
            for host in sorted(hosts):
                lines.append(f"- `{host}`")
        else:
            lines.append("- _No direct hosts, children only_")
        lines.append("")

    lines.append("## ⚙️ Group Variables")
    if group_vars:
        for group, vars_dict in group_vars.items():
            lines.append(f"### `{group}`")
            for var, val in vars_dict.items():
                lines.append(f"- `{var}`: `{val}`")
            lines.append("")
    else:
        lines.append("_No group variables defined._\n")

    lines.append("## 🖥 Host Variables")
    if host_vars:
        for host, vars_dict in host_vars.items():
            lines.append(f"### `{host}`")
            for var, val in vars_dict.items():
                lines.append(f"- `{var}`: `{val}`")
            lines.append("")
    else:
        lines.append("_No host variables defined._\n")

    lines.append("## 🧩 Group Children")
    if group_children:
        for group, children in group_children.items():
            lines.append(f"### `{group}`")
            for child in children:
                lines.append(f"- `{child}`")
            lines.append("")
    else:
        lines.append("_No child groups defined._\n")

    # Write per-inventory doc
    docs_dir.mkdir(parents=True, exist_ok=True)
    output_path = docs_dir / f"{inventory_name}.md"
    output_path.write_text("\n".join(lines))

    # Save meta for global index
    INVENTORY_META[inventory_name] = {
        "description": f"Inventory for `{inventory_name}` hosts",
        "doc_path": output_path
    }

# ------------------------------
# Write Global Index
# ------------------------------
def write_inventory_index(docs_dir: Path, inventory_root: Path):
    lines = ["# 🧭 Inventory Index\n"]
    lines.append("| Inventory | Description |")
    lines.append("|-----------|-------------|")
    # Build docs/inventories README (links local to docs_dir)
    docs_lines = list(lines)
    for name, meta in sorted(INVENTORY_META.items()):
        rel_path = meta["doc_path"].relative_to(docs_dir)
        docs_lines.append(f"| [`{name}`]({rel_path.as_posix()}) | {meta['description']} |")

    docs_lines.append("\n## 🖥 Global Host Index")
    docs_lines.append("| Host | Inventories | Groups |")
    docs_lines.append("|------|-------------|--------|")
    for host, info in sorted(HOST_INDEX.items()):
        inv_links = [f"[`{inv}`]({INVENTORY_META[inv]['doc_path'].relative_to(docs_dir).as_posix()})" for inv in info["inventories"]]
        docs_lines.append(f"| `{host}` | {', '.join(inv_links)} | {', '.join(sorted(info['groups']))} |")

    docs_lines.append("\n## ⚠️ Duplicate Hosts")
    docs_lines.append("> **📌 Note – Duplicate Hosts**\n>\n> Hosts appearing in multiple inventories may have conflicting variables or group memberships. Contributors should review these cases and consider refactoring to maintain a single authoritative definition per host.\n> Use `--strict` mode to enforce uniqueness.\n")

    docs_index_path = docs_dir / "README.md"
    content_docs = "\n".join(docs_lines)
    docs_index_path.write_text(content_docs)

    # Build inventory/README.md with links pointing to docs/inventories
    # Compute relative path from inventory_root to docs_dir (e.g. "../docs/inventories")
    rel_prefix = os.path.relpath(str(docs_dir), start=str(inventory_root))
    inv_lines = ["# 🧭 Inventory Index\n"]
    inv_lines.append("| Inventory | Description |")
    inv_lines.append("|-----------|-------------|")
    for name, meta in sorted(INVENTORY_META.items()):
        target = (Path(rel_prefix) / meta["doc_path"].name).as_posix()
        inv_lines.append(f"| [`{name}`]({target}) | {meta['description']} |")

    inv_lines.append("\n## 🖥 Global Host Index")
    inv_lines.append("| Host | Inventories | Groups |")
    inv_lines.append("|------|-------------|--------|")
    for host, info in sorted(HOST_INDEX.items()):
        inv_links = [f"[`{inv}`]({(Path(rel_prefix) / INVENTORY_META[inv]['doc_path'].name).as_posix()})" for inv in info["inventories"]]
        inv_lines.append(f"| `{host}` | {', '.join(inv_links)} | {', '.join(sorted(info['groups']))} |")

    inv_lines.append("\n## ⚠️ Duplicate Hosts")
    inv_lines.append(docs_lines[-3])

    inventory_index_path = inventory_root / "README.md"
    content_inv = "\n".join(inv_lines)
    inventory_index_path.write_text(content_inv)
    logging.info(f"Global inventory index written to {docs_index_path} and {inventory_index_path}")

# ------------------------------
# Main
# ------------------------------
def main():
    parser = argparse.ArgumentParser(description="Generate Ansible inventory documentation")
    parser.add_argument("--inventory", type=str, help="Path to a single inventory file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--strict", action="store_true", help="Halt on duplicate hosts")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    docs_dir = Path("docs/inventory")
    inventory_root = Path("inventory")

    if args.inventory:
        inv_path = Path(args.inventory)
        if not inv_path.exists():
            logging.error(f"Inventory file not found: {inv_path}")
            sys.exit(1)
        generate_inventory_doc(inv_path, docs_dir)
        report_duplicate_hosts(strict=args.strict)
        write_inventory_index(docs_dir, inventory_root)
        logging.info(f"Documentation generated for single inventory: {inv_path}")
        return

    # Traverse all inventory folders
    for inv_file in inventory_root.rglob("*.ini"):
        generate_inventory_doc(inv_file, docs_dir)

    report_duplicate_hosts(strict=args.strict)
    write_inventory_index(docs_dir, inventory_root)
    logging.info("Inventory documentation generation complete.")

if __name__ == "__main__":
    main()
