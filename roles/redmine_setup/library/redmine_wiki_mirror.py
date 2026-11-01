# plugins/modules/redmine_wiki_mirror.py

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.redmine_wiki import mirror_redmine_wiki

DOCUMENTATION = r"""
---
module: redmine_wiki_mirror
short_description: Mirror Redmine wiki pages into a local directory
version_added: "1.0.0"
author:
  - "Frank Refol (t3knoid)"
description:
  - Mirror Redmine wiki pages from a single project into a local directory.
  - This is a one-way mirror. Redmine is treated as the source of truth.
  - Local files are created, updated, or removed to exactly match the Redmine wiki state.
  - No changes are ever pushed back to Redmine.

options:
  redmine_url:
    type: str
    required: true
  project:
    type: str
    required: true
  api_key:
    type: str
    required: true
    no_log: true
  output_dir:
    type: str
    required: true
  delete_stale:
    type: bool
    default: true
  filename_extension:
    type: str
    default: "md"
  debug:
    description:
      - Enable verbose debug logging.
      - Debug messages are returned in C(debug_log).
    type: bool
    default: false
  rewrite_links:
    description:
      - Rewrite internal Redmine wiki links and wiki-style links to local filenames.
      - When true, wiki URLs and `[[Page]]` links are converted to Markdown links pointing
        at the mirrored filenames (the main wiki page `wiki` is written as index.md).
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Mirror Redmine wiki with debug enabled
  refol.general.redmine_wiki_mirror:
    redmine_url: https://redmine.example.com
    project: myproject
    api_key: "{{ redmine_api_key }}"
    output_dir: "{{ repo_path }}/wiki"
    debug: true
  register: mirror

- debug:
    var: mirror.debug_log
"""

RETURN = r"""
debug_log:
  description:
    - List of debug messages generated during the mirror operation.
  type: list
  elements: str
  returned: always
wiki_pages_found:
  description:
    - Number of wiki pages returned by the Redmine wiki index.
  type: int
  returned: always
"""


def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            redmine_url=dict(type="str", required=True),
            project=dict(type="str", required=True),
            api_key=dict(type="str", required=True, no_log=True),
            output_dir=dict(type="str", required=True),
            delete_stale=dict(type="bool", default=True),
            filename_extension=dict(type="str", default="md"),
            debug=dict(type="bool", default=False),
            rewrite_links=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    changed, synced, deleted, debug_log, wiki_pages_found = mirror_redmine_wiki(
        module,
        redmine_url=module.params["redmine_url"],
        project=module.params["project"],
        api_key=module.params["api_key"],
        output_dir=module.params["output_dir"],
        delete_stale=module.params["delete_stale"],
        filename_extension=module.params["filename_extension"],
      debug_enabled=module.params["debug"],
      rewrite_links=module.params["rewrite_links"],
    )

    module.exit_json(
        changed=changed,
        synced_pages=synced,
        deleted_pages=deleted,
        debug_log=debug_log,
        wiki_pages_found=wiki_pages_found,
    )


def main():
    run_module()


if __name__ == "__main__":
    main()