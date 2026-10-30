# Upgrading Ansible Python Modules

This guide describes how to review and update the pinned packages in `ansible_setup_python_modules` in `roles/ansible_setup/defaults/main/main.yml`.

## Check available versions

Use the Python interpreter for the target virtual environment. This avoids checking a different Python installation than the one used by Ansible:

```bash
/opt/python_3.12/bin/python -m pip index versions PACKAGE
```

Replace `PACKAGE` with the package name, for example `proxmoxer` or `psycopg2-binary`. Compare the `LATEST` and `INSTALLED` values with the version pinned in the role defaults. Repeat this for every direct package in `ansible_setup_python_modules`; checking a subset does not establish that the full list is current.

## Dry-run a candidate upgrade

Before changing a pin, ask pip to resolve the proposed version and its dependencies without installing it:

```bash
sudo /opt/python_3.12/bin/python -m pip install \
  --upgrade \
  --upgrade-strategy eager \
  "proxmoxer==2.3.0" \
  --dry-run
```

Substitute the package and candidate version. The supplied dry runs reported `Would install` for `proxmoxer==2.3.0`, `pycdlib==1.22.0`, `jmespath==1.1.0`, and `psycopg2-binary==2.9.13`. Review the complete resolver output, especially any changes to shared dependencies, before applying an upgrade. Use `sudo` only when required by ownership and permissions of the target environment.

`--upgrade-strategy eager` asks pip to consider upgrading dependencies as well as the requested package. A dry run is a resolver preview, not a compatibility test.

## Update and verify

1. Update the exact pins in `ansible_setup_python_modules` only after reviewing their candidate versions and dry-run results.
2. Keep any overlapping pins in the repository's root `requirements.txt` aligned when that file is intended to describe the same tool environment.
3. Apply the role to the intended host or environment.
4. Check dependency metadata and command startup:

   ```bash
   /opt/python_3.12/bin/python -m pip check
   /opt/python_3.12/bin/ansible-lint --version
   /opt/python_3.12/bin/ansible --version
   ```

5. For import errors involving packages also available from the OS, verify the modules resolve from the virtual environment rather than `/usr/lib/python3/dist-packages`:

   ```bash
   /opt/python_3.12/bin/python -c 'import jsonschema, referencing, rpds; print(jsonschema.__file__); print(referencing.__file__); print(rpds.__file__)'
   ```

The `/opt/python_3.12` environment enables system-site packages. Therefore, a clean `pip check` alone does not prove that imports are coming from the intended environment or that installed package files are healthy. Explicitly pinning a transitive dependency such as `jsonschema`, `referencing`, or `rpds-py` can ensure that pip installs it into the virtual environment rather than relying on an OS-provided copy.

Finally, run the relevant repository checks, including `ansible-lint` on the changed files, and review the dependency changes before merging.
