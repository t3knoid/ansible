# redmine_wiki_mirror

## Overview

`redmine_wiki_mirror` copies the wiki for one Redmine project into a local directory. Redmine is the source of truth: the module creates or updates local files for pages returned by Redmine and, when `delete_stale` is enabled, removes stale files with the configured extension. It does not write to Redmine or commit/push changes to a Git repository.

The module runs on the Ansible execution host for the task. The output directory is therefore on that host, which may be a managed host when the task uses privilege escalation.

## Requirements

- Ansible with `ansible.module_utils.urls.fetch_url` available.
- Redmine REST API access enabled.
- An API key for a user who can view the project's wiki.

## Behavior

1. Requests the project wiki index from `/projects/<project>/wiki/index.json`.
2. Requests each page from `/projects/<project>/wiki/<url-encoded-title>.json` and reads its `wiki_page.text` value. No `include=content` query parameter is used.
3. Writes each page as a Markdown-style text file in `output_dir`. Titles are lowercased and spaces become underscores; the default extension is `.md`. A page titled `wiki` is written as `index.<extension>`.
4. Adds YAML front matter containing a title when the content does not already start with front matter. Fenced code blocks are wrapped in Jekyll raw tags.
5. Optionally rewrites Redmine wiki URLs, bare Markdown links, and `[[Wiki links]]` to local filenames when `rewrite_links` is enabled.
6. Optionally deletes stale files matching `*.${filename_extension}` in the output directory. `README.md` is excluded from deletion.

The module fails if an HTTP request fails, JSON cannot be parsed, the index response does not contain a list of `wiki_pages`, or a page response does not contain non-empty `wiki_page.text`. A valid empty index is accepted as a wiki with no pages.

In check mode, file writes and deletions are skipped, but the module reports whether it would change files and returns the planned page paths.

## Options

| Setting | Values | Default | Setting Description |
| --- | --- | --- | --- |
| `redmine_url` | URL | Required | Base URL of the Redmine instance, for example `https://redmine.example.com`. |
| `project` | Project identifier or ID | Required | Redmine project whose wiki is mirrored. |
| `api_key` | String | Required | Redmine API key sent in the `X-Redmine-API-Key` header. The module marks it `no_log`. |
| `output_dir` | Path | Required | Directory in which page files are created, updated, or deleted. Created if it does not exist. |
| `delete_stale` | `true`, `false` | `true` | Remove files with the configured extension that are not in the returned wiki index. |
| `filename_extension` | Extension without leading dot | `md` | Extension used for mirrored files. |
| `debug` | `true`, `false` | `false` | Return request URLs, HTTP statuses, and page processing messages in `debug_log`. Response bodies are included in fetch errors, not normal debug output. |
| `rewrite_links` | `true`, `false` | `false` | Rewrite recognized internal Redmine and wiki-style links to local file links. |

## Example

```yaml
- name: Mirror Redmine wiki
  redmine_wiki_mirror:
    redmine_url: "https://redmine.example.com"
    project: myproject
    api_key: "{{ redmine_api_key }}"
    output_dir: /srv/docs/redmine
    delete_stale: true
    filename_extension: md
    rewrite_links: true
    debug: true
  register: redmine_mirror

- name: Report mirror result
  ansible.builtin.debug:
    msg:
      - "Pages found: {{ redmine_mirror.wiki_pages_found }}"
      - "Pages synced: {{ redmine_mirror.synced_pages | length }}"
      - "Pages deleted: {{ redmine_mirror.deleted_pages | length }}"
```

## Returned Values

| Key | Type | Description |
| --- | --- | --- |
| `changed` | Boolean | Whether files were or would be created, updated, or deleted. |
| `wiki_pages_found` | Integer | Number of entries returned in the Redmine wiki index. |
| `synced_pages` | List of paths | Files created or updated, or planned in check mode. |
| `deleted_pages` | List of paths | Stale files deleted, or planned for deletion in check mode. |
| `debug_log` | List of strings | Request and processing messages; empty unless `debug` is enabled. |

## Troubleshooting

- If `wiki_pages_found` is zero, verify the project identifier, the API key, the user's wiki visibility, and that REST API access is enabled. The module accepts an empty index as a successful response.
- If pages are found but no files are synced, check `synced_pages`, check mode, and whether the existing files already match Redmine. Confirm `output_dir` is on the host where the module runs and is writable by the task's effective user.
- Enable `debug` to see the requested index/page URLs and HTTP statuses. Request failures include the response body and response information in the Ansible failure result.

## Testing

Validate a playbook that uses it with `ansible-playbook --syntax-check <playbook>`, then run the task against a test project with a read-only API key and `debug: true`. Review `wiki_pages_found`, `synced_pages`, `deleted_pages`, and `debug_log` in the task result. A syntax check does not exercise the Redmine API or verify page content.