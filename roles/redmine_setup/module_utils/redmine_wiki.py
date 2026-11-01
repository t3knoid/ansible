# plugins/module_utils/redmine_wiki.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple
import re
from urllib.parse import unquote

from ansible.module_utils.urls import fetch_url
from urllib.parse import quote


class RedmineWikiMirrorError(Exception):
    pass


def _debug(debug_enabled: bool, log: List[str], message: str):
    if debug_enabled:
        log.append(message)


def _get_json(module, url: str, headers: Dict[str, str], debug_enabled: bool, log: List[str]) -> Dict:
    _debug(debug_enabled, log, f"Fetching URL: {url}")

    resp, info = fetch_url(module, url, headers=headers)
    status = info.get("status", 0)

    _debug(debug_enabled, log, f"HTTP status: {status}")

    if status != 200:
        body = ""
        if resp is not None:
            try:
                body = resp.read().decode("utf-8", errors="replace")
            except Exception:
                body = "<unable to decode response body>"

        module.fail_json(
            msg=f"Failed to fetch URL '{url}' (status={status})",
            response_body=body,
            response_info=info,
            debug_log=log,
        )

    try:
        raw = resp.read()
        return json.loads(raw)
    except Exception as e:
        module.fail_json(
            msg=f"Failed to parse JSON from '{url}': {e}",
            debug_log=log,
        )


def _default_filename(title: str, extension: str = "md") -> str:
    safe = title.replace(" ", "_").lower()
    return f"{safe}.{extension}"


def _normalize_title_key(title: str) -> str:
    """Normalize a wiki title for robust mapping lookups.

    Strips surrounding whitespace, replaces common non-standard hyphens
    with normal hyphens, collapses repeated whitespace, and lowercases.
    """
    if title is None:
        return ""
    t = title.strip()
    t = t.replace("\u2011", "-")
    t = re.sub(r"\s+", " ", t)
    return t.lower()


def _filename_for_title(title: str, extension: str = "md") -> str:
    """Return the filename to write for a given wiki title.

    Special-case the main wiki page (title 'wiki') to map to index.<ext>
    so repositories that consume the mirrored pages (e.g., GitHub) get
    a index as the project landing page.
    """
    if title and title.strip().lower() == "wiki":
        return f"index.{extension}"
    return _default_filename(title, extension)


def _ensure_front_matter(content: str, page_title: str) -> str:
    """Ensure the markdown content begins with a YAML front matter containing the page title.

    The function will leave the content unchanged if it already starts with a YAML front
    matter delimiter (`---`). Otherwise it will prepend a minimal front matter with a
    `title` field derived from the page's main markdown title (or the supplied title
    if no markdown heading is present).
    """
    if content is None:
        content = ""

    # If the file already contains front matter, assume it's intentional and do nothing.
    if re.match(r"^\s*---", content):
        return content

    # Try to extract the first Markdown H1 ("# Title")
    m = re.search(r"^\s*#\s+(.+)", content, flags=re.MULTILINE)
    if m:
        main_title = m.group(1).strip()
    else:
        # Fallback to Setext-style H1 (Title\n====)
        m2 = re.search(r"^([^\n]+)\n=+\s*$", content, flags=re.MULTILINE)
        if m2:
            main_title = m2.group(1).strip()
        else:
            main_title = page_title or ""

    # Sanitize and escape title for safe YAML quoting
    def _sanitize_title_for_front_matter(t: str) -> str:
        if t is None:
            return ""
        s = t.strip()
        # Remove any leading Markdown header markers (e.g. '# Title')
        s = re.sub(r"^#+\s*", "", s)
        # Remove YAML front-matter delimiters if present
        s = s.replace("---", "")
        # Remove common Unicode emoji ranges (broad coverage)
        emoji_re = re.compile(
            "[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]+",
            flags=re.UNICODE,
        )
        s = emoji_re.sub("", s)
        # Remove common ASCII emoticons like :-) :( :D etc.
        s = re.sub(r"[:;=8][\-~]?[)DdpP\(\]/\\]", "", s)
        # Remove inline code markers and emphasis markers (but keep underscores)
        s = s.replace('`', '')
        s = s.replace('*', '')
        # Remove non-printable/control characters
        s = ''.join(ch for ch in s if ch.isprintable())
        # Collapse whitespace
        s = re.sub(r"\s+", " ", s)
        return s.strip()

    safe_title_raw = _sanitize_title_for_front_matter(main_title or page_title or "")
    safe_title = safe_title_raw.replace('"', '\\"')

    front_matter = f"---\ntitle: \"{safe_title}\"\n---\n\n"

    return front_matter + content.lstrip("\n")


def _rewrite_content(content: str, project: str, base: str, mapping: Dict[str, str], extension: str = "md") -> str:
    """Rewrite known Redmine wiki links and wiki-style links to local filenames.

    - Rewrites absolute or relative Redmine wiki URLs to the mapped filename.
    - Rewrites wiki-style links [[Page]] or [[Page|Label]] to Markdown links.
    - Rewrites bare Markdown links where the target is a wiki title.
    """

    # Replace full or site-relative Redmine wiki links
    # e.g. https://host/projects/<project>/wiki/<title>
    pattern_full = re.compile(r'https?://[^\s)\'"\]]+/projects/' + re.escape(project) + r'/wiki/([^\)\s\'"\]]+)')

    def _replace_full(m):
        enc = m.group(1)
        title = unquote(enc)
        fname = (
            mapping.get(title)
            or mapping.get(enc)
            or mapping.get(_normalize_title_key(title))
            or mapping.get(_normalize_title_key(enc))
            or _default_filename(title, extension=extension)
        )
        return fname

    content = pattern_full.sub(lambda m: _replace_full(m), content)

    # Replace site-relative links: /projects/<project>/wiki/<title>
    pattern_rel = re.compile(r'/projects/' + re.escape(project) + r'/wiki/([^\)\s\'"\]]+)')

    def _replace_rel(m):
        raw = m.group(1)
        title = unquote(raw)
        return (
            mapping.get(title)
            or mapping.get(raw)
            or mapping.get(_normalize_title_key(title))
            or mapping.get(_normalize_title_key(raw))
            or _default_filename(title, extension=extension)
        )

    content = pattern_rel.sub(lambda m: _replace_rel(m), content)

    # Rewrite wiki-style links [[Title]] or [[Title|Label]]
    wiki_link_re = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

    # Rewrite Markdown links where the target is a bare wiki title,
    # e.g. [Label](Proxmox) -> [Label](proxmox.md)
    md_link_re = re.compile(r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)')

    def _md_link_replace(m):
        label = m.group(1)
        target = m.group(2).strip()
        # Skip external, absolute, anchors, mailto, or already-file targets
        if re.match(r'^(?:https?:)?//', target) or target.startswith('/') or target.startswith('#') or ':' in target or '.' in target:
            return m.group(0)

        fname = (
            mapping.get(target)
            or mapping.get(_normalize_title_key(target))
            or mapping.get(quote(target, safe=""))
            or None
        )
        if not fname:
            fname = _default_filename(target, extension=extension)

        if not fname.lower().startswith(f"index.{extension}"):
            fname = fname.lower()

        return f"[{label}]({fname})"

    # We need quote here for lookup; import inside to avoid unused if function not used
    from urllib.parse import quote

    # First rewrite bare Markdown links, then wiki-style links
    content = md_link_re.sub(_md_link_replace, content)

    def _wiki_link_replace(m):
        title = m.group(1).strip()
        label = m.group(2) or title
        fname = (
            mapping.get(title)
            or mapping.get(_normalize_title_key(title))
            or mapping.get(quote(title, safe=''))
            or _default_filename(title, extension=extension)
        )
        if not fname.lower().startswith(f"index.{extension}"):
            fname = fname.lower()
        return f"[{label}]({fname})"

    content = wiki_link_re.sub(_wiki_link_replace, content)

    return content


def _wrap_fenced_code_blocks_with_raw(content: str) -> str:
    """Wrap fenced code blocks with Jekyll raw tags to avoid Liquid parsing.

    This inserts a `{% raw %}` immediately after the opening fence and a
    `{% endraw %}` immediately before the closing fence for each fenced
    code block (```) found in the content. Blocks already containing raw
    tags are left unchanged.
    """
    if content is None:
        return content

    # Match fenced code blocks: opening fence (``` optionally with language),
    # code, then closing fence. Use DOTALL so code can contain newlines.
    pattern = re.compile(r"(^```[^\n]*\n)(.*?)(\n```)", re.DOTALL | re.MULTILINE)

    def _repl(m):
        full = m.group(0)
        open_fence = m.group(1)
        code = m.group(2)
        close_fence = m.group(3)

        # If the matched block already contains raw tags, don't double-wrap.
        if "{% raw %}" in full or "{% endraw %}" in full:
            return full

        # Wrap the entire fenced block with raw tags (outside the backticks).
        return f"{{% raw %}}\n{open_fence}{code}{close_fence}\n{{% endraw %}}"

    return pattern.sub(_repl, content)


def mirror_redmine_wiki(
    module,
    *,
    redmine_url: str,
    project: str,
    api_key: str,
    output_dir: str,
    delete_stale: bool = True,
    filename_extension: str = "md",
    debug_enabled: bool = False,
    rewrite_links: bool = False,
) -> Tuple[bool, List[str], List[str], List[str], int]:
    """
    Returns: (changed, synced_pages, deleted_pages, debug_log, wiki_pages_found)
    """
    log: List[str] = []

    headers = {"X-Redmine-API-Key": api_key}
    base = redmine_url.rstrip("/")

    index_url = f"{base}/projects/{project}/wiki/index.json"
    index_response = _get_json(module, index_url, headers, debug_enabled, log)
    index_value = index_response.get("wiki_pages")
    if not isinstance(index_value, list):
        module.fail_json(
            msg="Redmine returned an invalid wiki index response",
            response_fields=sorted(index_response.keys()),
            debug_log=log,
        )
        raise RedmineWikiMirrorError("Redmine returned an invalid wiki index response")
    index: List[Dict] = index_value

    # Build title -> filename mapping for all pages up-front so links can be rewritten.
    title_to_filename: Dict[str, str] = {}
    for entry in index:
        t = entry.get("title")
        if not t:
            continue
        fname = _filename_for_title(t, extension=filename_extension)
        title_to_filename[t] = fname
        title_to_filename[_normalize_title_key(t)] = fname

    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    _debug(debug_enabled, log, f"Output directory: {outdir}")

    changed = False
    seen_filenames = set()
    synced_pages: List[str] = []
    deleted_pages: List[str] = []

    # Mirror wiki pages
    for entry in index:
        title = entry.get("title")
        if not title:
            _debug(debug_enabled, log, "Skipping entry with no title")
            continue

        filename = _filename_for_title(title, extension=filename_extension)
        seen_filenames.add(filename)

        _debug(debug_enabled, log, f"Processing page '{title}' → {filename}")

        encoded_title = quote(title, safe="")
        page_url = f"{base}/projects/{project}/wiki/{encoded_title}.json"
        page_response = _get_json(module, page_url, headers, debug_enabled, log)
        page = page_response.get("wiki_page")
        if not isinstance(page, dict):
            module.fail_json(
                msg=f"Redmine returned no wiki text for page '{title}'",
                response_fields=sorted(page_response.keys()),
                wiki_page_fields=[],
                debug_log=log,
            )
            raise RedmineWikiMirrorError(f"Redmine returned no wiki text for page '{title}'")
        content = page.get("text")
        if not isinstance(content, str) or not content:
            module.fail_json(
                msg=f"Redmine returned no wiki text for page '{title}'",
                response_fields=sorted(page_response.keys()),
                wiki_page_fields=sorted(page.keys()),
                debug_log=log,
            )
            raise RedmineWikiMirrorError(f"Redmine returned no wiki text for page '{title}'")

        if rewrite_links:
            try:
                content = _rewrite_content(content, project, base, title_to_filename, extension=filename_extension)
            except Exception as e:
                _debug(debug_enabled, log, f"Link rewrite failed for '{title}': {e}")
        # Wrap fenced code blocks with Jekyll raw tags to avoid Liquid parsing errors
        try:
            content = _wrap_fenced_code_blocks_with_raw(content)
        except Exception as e:
            _debug(debug_enabled, log, f"Code block wrapping failed for '{title}': {e}")
        # Ensure the generated markdown has a YAML front matter with the page title.
        final_content = _ensure_front_matter(content, title)

        fpath = outdir / filename

        old_content = ""
        if fpath.exists():
            try:
                old_content = fpath.read_text(encoding="utf-8")
            except Exception:
                old_content = None

        if old_content != final_content:
            _debug(debug_enabled, log, f"Writing updated content to {fpath}")
            if not module.check_mode:
                fpath.write_text(final_content, encoding="utf-8")
            changed = True
            synced_pages.append(str(fpath))
        else:
            _debug(debug_enabled, log, f"No change for {fpath}")

    # Delete stale files
    if delete_stale:
        for f in outdir.glob(f"*.{filename_extension}"):
            if f.name not in seen_filenames and f.name != "README.md":
                _debug(debug_enabled, log, f"Deleting stale file {f}")
                if not module.check_mode:
                    f.unlink()
                changed = True
                deleted_pages.append(str(f))

    return changed, synced_pages, deleted_pages, log, len(index)