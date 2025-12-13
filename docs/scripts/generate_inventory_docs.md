#!/usr/bin/env python3
import argparse
from collections import defaultdict
from configparser import ConfigParser
from pathlib import Path
import logging
import sys

logging.basicConfig(level=logging.INFO)

# Global structures
HOST_INDEX = defaultdict(lambda: {"inventories": set(), "groups": set()})
INVENTORY_META = {}

def parse_ini_inventory(file_path: Path):
    """
    Parse an INI-style inventory file and return hosts and group mappings.
    Hosts with inline variables are handled correctly.
    """
    parser = ConfigParser(allow_no_value=True, delimiters=("=",))
    parser.optionxform = str  # preserve case
    with file_path.open() as f:
        content = f.read()

    # ConfigParser expects section headers, so prepend dummy if missing
    if not content.strip().startswith("["):
        content = "[all]\n" + content

    parser.read_string(content)

    inventory_name = file_path.parent.name
    INVENTORY_META[inventory_name] = {
        "doc_path": Path(f"docs/inventory/{inventory_name}.md"),
        "description": f"Inventory for {inventory_name}"
    }

    for section in parser.sections():
        for item in parser.items(section):
            # Split only on first space to separate host name from variables
            host_line = item[0]
            host = host_line.split()[0]
            HOST_INDEX[host]["inventories"].add(inventory_name)
            HOST_INDEX[host]["groups"].add(section)

def generate_inventory_markdown(inventory_name: str):
    """Generate per-inventory Markdown documentation."""
    doc_path = Path(f"docs/inventory/{inventory_name}.md")
    lines = [f"# 🖥 Inventory: `{inventory_name}`\n"]

    lines.append("## Hosts")
    hosts = [h for h, info in HOST_INDEX.items() if inventory_name in info["inventories"]]
    if hosts:
        for host in sorted(hosts):
            groups = ", ".join(sorted(HOST_INDEX[host]["groups"]))
            lines.append(f"- `{host}` ({groups})")
    else:
        lines.append("_No hosts defined._")

    lines.append("\n## Groups")
    groups = set()
    for h in hosts:
        groups.update(HOST_INDEX[h]["groups"])
    if groups:
        for group in sorted(groups):
            lines.append(f"- `{group}`")
    else:
        lines.append("_No groups defined._")

    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text("\n".join(lines))

def write_inventory_index(docs_dir: Path, inventory_root: Path):
    """Generate global inventory index with 📌 pin for inventories with multiple hosts."""
    lines = ["# 📚 Inventory Index\n", "| Inventory | Description |", "|-----------|-------------|"]
    for name, meta in sorted(INVENTORY_META.items()):
        # Determine host count
        host_count = sum(1 for h, info in HOST_INDEX.items() if name in info["inventories"])
        pin = " 📌" if host_count > 1 else ""
        rel_path = meta["doc_path"].relative_to(docs_dir)
        lines.append(f"| [`{name}`]({rel_path}){pin} | {meta['description']} |")

    index_content = "\n".join(lines)
    # Write to both docs/inventory and inventory root
    (docs_dir / "README.md").write_text(index_content)
    (inventory_root / "README.md").write_text(index_content)

def main():
    parser = argparse.ArgumentParser(description="Generate Ansible inventory documentation")
    parser.add_argument("--inventory", type=str, help="Path to single inventory file for debugging")
    parser.add_argument("--strict", action="store_true", help="Enforce unique host definitions")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    docs_dir = Path("docs/inventory")
    docs_dir.mkdir(parents=True, exist_ok=True)
    inventory_root = Path("inventory")

    inventory_files = []

    if args.inventory:
        inv_path = Path(args.inventory)
        if not inv_path.exists():
            logging.error(f"Inventory file {inv_path} does not exist.")
            sys.exit(1)
        inventory_files = [inv_path]
    else:
        inventory_files = list(inventory_root.rglob("inventory.ini"))

    for inv_file in inventory_files:
        logging.debug(f"Parsing inventory file: {inv_file}")
        parse_ini_inventory(inv_file)

    # Duplicate host detection
    duplicates = False
    for host, info in HOST_INDEX.items():
        if len(info["inventories"]) > 1:
            logging.warning(f"Duplicate host detected: {host} in inventories: {', '.join(sorted(info['inventories']))}")
            duplicates = True

    if args.strict and duplicates:
        logging.error("Strict mode enabled: duplicate hosts found, exiting.")
        sys.exit(1)

    # Generate per-inventory docs
    for inv_name in INVENTORY_META:
        logging.debug(f"Generating Markdown for inventory: {inv_name}")
        generate_inventory_markdown(inv_name)

    # Generate global index
    write_inventory_index(docs_dir, inventory_root)
    logging.info("Inventory documentation generation complete.")

if __name__ == "__main__":
    main()
