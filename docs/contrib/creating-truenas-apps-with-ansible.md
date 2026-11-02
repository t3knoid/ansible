# 📦 Creating TrueNAS Apps with Ansible

## 📖 Purpose

This explains how to declare a TrueNAS application in the inventory and deploy it with the `truenas` role. It covers:

1. choosing between a **catalog** app and a **custom** (Compose) app
2. finding the correct `values` for a catalog app from its schema
3. storing secrets in the host Vault
4. planning, applying, upgrading, and removing the app

It uses two worked examples: a  **Postgres** app and a **Nexdeck** app. The two have different `values`, and the guide explains why so you can configure any other catalog app.

For the role's general design, see the [TrueNAS role contributor guide](truenas-role-contributor-guide.md#-apps).

---

## 🧭 How App Deployment Works Here

Apps are **not** part of `configure_truenas.yml`. They have their own playbook, [`playbooks/truenas/deploy_truenas_apps.yml`](../../playbooks/truenas/deploy_truenas_apps.yml), which imports [`roles/truenas/tasks/apps.yml`](../../roles/truenas/tasks/apps.yml).

For each entry in `truenas_apps`, the workflow:

1. validates every declaration locally ([`apps_validate.yml`](../../roles/truenas/tasks/apps_validate.yml)) before it contacts the NAS
2. runs the read-only preflight and checks that an Apps storage pool exists (`docker.config`)
3. calls the `truenas_api` module in `mode: app` ([`library/truenas_api.py`](../../roles/truenas/library/truenas_api.py)), which:
   - creates the app with `app.create` when it does not exist
   - compares your `values` with `app.config <name>` and calls `app.update` only when they differ
   - calls `app.upgrade` when `catalog.version` changes, but only if you set `allow_upgrade: true`
   - starts or stops the app to match `runtime`
   - waits for each middleware job, then waits for the app to reach `RUNNING` or `STOPPED`

`truenas_apps_mode` defaults to `plan`, so the playbook only reports what it would do. Nothing changes until you pass `-e truenas_apps_mode=apply`. Ansible check mode (`--check`) is always read-only.

App declarations go in [`inventory/truenas/host_vars/truenas-01/default.yml`](../../inventory/truenas/host_vars/truenas-01/default.yml). Secrets go in `inventory/truenas/host_vars/truenas-01/vault.yml`.

---

## 🧱 Anatomy of an App Entry

Every entry in `truenas_apps` accepts only these top-level keys. Any other key fails validation.

| Key | Required | Values | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | Yes | `^[a-z]([-a-z0-9]*[a-z0-9])?$`, max 40 chars | — | The TrueNAS app instance name. It must be unique in the list and becomes the app ID in the UI, `midclt`, and ix-volume dataset paths. |
| `source` | Yes | `catalog`, `custom` | — | `catalog` installs an app from a TrueNAS catalog train. `custom` deploys your own Compose YAML. |
| `state` | No | `present`, `absent` | `present` | `absent` deletes the app, and requires `allow_delete: true`. |
| `runtime` | No | `running`, `stopped` | `running` | The desired container state after reconciliation. |
| `catalog` | Catalog only | mapping | — | `app`, `train`, and `version`, described below. |
| `values` | Catalog only | mapping | `{}` | App-specific settings. **The structure is different for every catalog app.** |
| `compose` | Custom only | YAML string | — | A Compose file with a non-empty `services` mapping. |
| `allow_upgrade` | No | boolean | `false` | Permits a change to `catalog.version`. |
| `allow_delete` | No | boolean | `false` | Permits `state: absent`. Images and ix volumes are kept. |

### `catalog` block

| Key | Example | Where to find it |
| --- | --- | --- |
| `app` | `nexdeck` | The catalog app name: the directory name under `ix-dev/<train>/` in the [truenas/apps](https://github.com/truenas/apps) repo, or the `name` field from `app.available`. |
| `train` | `community` | The directory the app lives in: `stable`, `community`, `enterprise`, or `test`. |
| `version` | `"1.0.42"` | The **catalog (chart) version**, the `version:` field in `app.yaml`. It is **not** `app_version`, which is the upstream software version. Always quote it, and never use `latest`. |

> ⚠️ `app` and `train` cannot change after the app is created. The role refuses to replace an app from a different catalog entry. Delete it and create it again instead.

---

## 🔍 Finding the Correct `values` for a Catalog App

This is the step that differs between apps. **`values` is not a fixed role schema.** It is the answer set for that app's `questions.yaml` in the TrueNAS catalog. Postgres asks different questions than Nexdeck, so copying the Postgres block will not work.

### Step 1: Get the app's schema

Use either source. Both give the same schema for the same version.

**Option A: GitHub (no NAS access needed).** Open:

```text
https://github.com/truenas/apps/tree/master/ix-dev/<train>/<app>/
```

- `app.yaml` has `version` (use this for `catalog.version`), `app_version`, `train`, `host_mounts`, and `run_as_context`.
- `questions.yaml` is the schema for `values`.

`master` holds the latest version. If you pin an older `catalog.version`, check that the schema has not changed since.

**Option B: The NAS itself** (SSH as an admin user; see the [midclt cheat sheet](midclt-cheats-sheet-for-truenas.md)):

```bash
# Confirm the app exists, and see its train and latest catalog version
midclt call app.available '[["name","=","nexdeck"]]' '{"select":["name","train","latest_version","latest_app_version"]}'

# Full details, including the questions schema for each available version
midclt call catalog.get_app_details nexdeck '{"train":"community"}' | jq '.versions | keys'
midclt call catalog.get_app_details nexdeck '{"train":"community"}' | jq '.versions["1.0.42"].schema.questions'
```

### Step 2: Translate `questions.yaml` into YAML `values`

Each question is a `variable`. The `variable` names become your `values` keys, and nesting follows `schema.type: dict` → `attrs`.

| `questions.yaml` element | Meaning for your `values` |
| --- | --- |
| `group:` | UI grouping only. **It is not a key.** Ignore it. |
| `variable: foo` at top level | A top-level key under `values:` (`values.foo`). |
| `type: dict` + `attrs:` | A nested mapping. Each `attrs[].variable` is a child key. |
| `type: list` + `items:` | A YAML list. The single `items[]` entry describes one element. Its `variable` name, such as `env` or `host_ip`, is **not** a key. |
| `type: int` | An unquoted integer. `"4096"` is a string and causes permanent drift. |
| `type: boolean` | `true` or `false`, unquoted. |
| `type: string`, `uri`, `path`, `hostpath` | A string. |
| `default:` | The value TrueNAS uses if you omit the key. |
| `required: true` | Must have a valid value. If the default is empty (`""`), **you must supply one**. |
| `enum:` | Only the listed `value:` entries are accepted. `""` is a real option in some enums. |
| `min`, `max`, `min_length` | Validation limits enforced by middleware. |
| `show_if:` | The key only applies when the condition holds. For example, `ix_volume_config` applies only when `type: ix_volume`. |
| `hidden: true` | Not shown in the UI. Leave it at its default unless you know why you need to change it. |
| `private: true` | A secret. Put it in Vault. |
| `$ref: definitions/timezone` | A string timezone such as `America/New_York`. |
| `$ref: definitions/node_bind_ip` | A host IP address on the NAS, or `0.0.0.0`. |

### Step 3: Decide what to declare

Values are **merged** into the app's current configuration. The role only compares and updates the keys you list:

- **On create**, TrueNAS fills in the schema default for every key you omit. You must still supply any `required` key whose default is empty or invalid.
- **On later runs**, keys you leave out are not managed. Changes made in the UI to those keys are not reverted.

**Recommendation:** declare every setting you care about (secrets, ports, storage, resources, timezone), and leave UI-only or rarely used keys such as `labels` and `networks` at their defaults.

### Comparison rules to keep in mind

The module compares desired and current values strictly ([`app_config_matches`](../../roles/truenas/library/truenas_api.py)):

- **Types must match exactly.** `port_number: 30495` matches, but `port_number: "30495"` is reported as a change on every run.
- **Lists are compared in order and by length.** List `host_ips` in the same order every time.
- **Mappings are compared one way.** Extra keys that TrueNAS returns are ignored. Missing keys are not.

If a plan reports `update` on every run, compare your entry with `midclt call app.config <name>` and look for a type or ordering mismatch.

---

## 🐘 Example 1: Postgres (existing)

The schema for `ix-dev/community/postgres` has top-level questions `postgres`, `run_as`, `network`, `storage`, `labels`, and `resources`. Its network question is called **`tcp_port`**, and its data volume is `storage.data`.

```yaml
truenas_apps:
  - name: postgres
    source: catalog
    state: present
    runtime: running
    catalog:
      app: postgres
      train: community
      version: "1.5.46"
    values:
      postgres:                       # app-specific block
        image_selector: v18_image
        user: postgres
        password: "{{ vault_truenas_postgres_password }}"
        database: postgres
        shm_size_mb: 512
      resources:
        limits:
          cpus: 2
          memory: 4096
      network:
        host_network: false
        tcp_port:                     # Postgres calls its port "tcp_port"
          bind_mode: published
          port_number: 5432
          host_ips:
            - "0.0.0.0"
      storage:
        data:
          type: ix_volume
          ix_volume_config:
            acl_enable: false
            dataset_name: data
```

---

## 🗂️ Example 2: Nexdeck (new)

Nexdeck is a homelab dashboard in the **community** train. From [`ix-dev/community/nexdeck/app.yaml`](https://github.com/truenas/apps/tree/master/ix-dev/community/nexdeck):

| Field | Value | Use |
| --- | --- | --- |
| `name` | `nexdeck` | `catalog.app` |
| `train` | `community` | `catalog.train` |
| `version` | `1.0.42` | `catalog.version` |
| `app_version` | `1.2.0` | The upstream Nexdeck release. For reference only. |
| `run_as_context` | uid/gid `568` (`apps`) | The default `run_as` values. |
| `host_mounts` | `/var/run/docker.sock` | Mounted only when `nexdeck.docker_socket: true`. |

### How Nexdeck differs from Postgres

| Area | Postgres | Nexdeck |
| --- | --- | --- |
| App-specific block | `values.postgres` (`user`, `password`, `database`, `image_selector`, `shm_size_mb`) | `values.nexdeck` (`secret_key`, `public_url`, `docker_socket`, `additional_envs`) |
| Timezone | — | **Top-level `values.TZ`** (uppercase), required, default `Etc/UTC` |
| Required secret | `postgres.password` | `nexdeck.secret_key`, **minimum 16 characters**, required, empty default |
| Port key | `network.tcp_port` | **`network.web_port`** |
| Default port | `5432` | `30495` |
| Data dataset name | `data` | `config` (hidden in the UI; leave it as is) |

### Nexdeck values reference

Settings from `questions.yaml` for catalog version `1.0.42`:

| Key path under `values` | Type | Default | Required | Notes |
| --- | --- | --- | --- | --- |
| `TZ` | string | `Etc/UTC` | Yes | A timezone name, for example `America/Chicago`. |
| `nexdeck.secret_key` | string (private) | `""` | **Yes**, min 16 chars | Signs sessions and **encrypts the stored credentials** for every service Nexdeck connects to. Changing it later signs everyone out and makes saved connections unreadable. Generate it once and keep it in Vault. |
| `nexdeck.public_url` | uri | `""` | No | The URL browsers use, such as `https://nexdeck.refol.us`. Needed for identity-provider sign-in and Web Push. It can also be set in the Nexdeck UI. |
| `nexdeck.docker_socket` | boolean | `false` | No | Mounts `/var/run/docker.sock` so Nexdeck can list, start, stop, and tail containers on the NAS. **Socket access gives root on the host.** Enable it only if you need it. |
| `nexdeck.additional_envs` | list of `{name, value}` | `[]` | No | Extra container environment variables. |
| `run_as.user` | int, ≥ 568 | `568` | Yes | The UID that owns Nexdeck files. |
| `run_as.group` | int, ≥ 568 | `568` | Yes | The GID that owns Nexdeck files. |
| `network.host_network` | boolean | `false` | No | Keep this `false`. |
| `network.web_port.bind_mode` | `published`, `exposed`, `""` | `published` | No | `published` makes the port reachable from the LAN. |
| `network.web_port.port_number` | int, 1–65535 | `30495` | Yes | The host port for the web UI. It must not conflict with other apps or services. |
| `network.web_port.host_ips` | list of IPs | `[]` | No | Applies only when `published`. An empty list binds all IPs. |
| `network.networks` | list | `[]` | No | Existing Docker networks to join. Usually left unset. |
| `storage.data.type` | `ix_volume`, `host_path` | `ix_volume` | Yes | Holds the SQLite database, uploads, and generated keys. |
| `storage.data.ix_volume_config.dataset_name` | string | `config` | Yes (hidden) | Keep `config`. |
| `storage.data.ix_volume_config.acl_enable` | boolean | `false` | No | |
| `storage.data.host_path_config.path` | hostpath | — | When `host_path` | An existing dataset path, such as `/mnt/Data/configs/nexdeck`. It must be writable by `run_as` (568:568). |
| `storage.additional_storage` | list | `[]` | No | Extra `ix_volume`, `host_path`, `cifs`, or `nfs` mounts, each with `mount_path`. |
| `labels` | list | `[]` | No | Docker labels on the `nexdeck` container. |
| `resources.limits.cpus` | int | `2` | Yes | |
| `resources.limits.memory` | int (MB) | `4096` | Yes | |

### Step 1: Add the secret to Vault

Generate a key of at least 16 characters:

```bash
openssl rand -hex 32
```

Add it to the host Vault:

```bash
ansible-vault edit inventory/truenas/host_vars/truenas-01/vault.yml
```

```yaml
vault_truenas_nexdeck_secret_key: "<paste the generated value>"
```

### Step 2: Add the app to `truenas_apps`

Add a **second, distinct** entry next to Postgres in `inventory/truenas/host_vars/truenas-01/default.yml`. Each `name` can appear only once, so a copied `postgres` entry fails validation with *"Each TrueNAS application name must appear exactly once."*

```yaml
truenas_apps:
  - name: postgres
    # ... unchanged ...

  - name: nexdeck
    source: catalog
    state: present
    runtime: running
    catalog:
      app: nexdeck
      train: community
      version: "1.0.42"
    values:
      TZ: America/Chicago
      nexdeck:
        secret_key: "{{ vault_truenas_nexdeck_secret_key }}"
        public_url: https://nexdeck.refol.us
        docker_socket: false
      run_as:
        user: 568
        group: 568
      network:
        host_network: false
        web_port:
          bind_mode: published
          port_number: 30495
          host_ips:
            - "0.0.0.0"
      storage:
        data:
          type: ix_volume
          ix_volume_config:
            acl_enable: false
            dataset_name: config
      resources:
        limits:
          cpus: 2
          memory: 2048
```

Replace `TZ`, `public_url`, and the memory limit with your own values. Delete `public_url` if you have no reverse-proxy name yet.

#### Variant: store data on an existing dataset

Use this if you want Nexdeck's data on a dataset you manage and snapshot, instead of an ix volume. The path must already exist; create it with `truenas_datasets` if needed.

```yaml
      storage:
        data:
          type: host_path
          host_path_config:
            acl_enable: false
            path: /mnt/Data/configs/nexdeck
```

> ⚠️ Do not switch `storage.data.type` on an app that already has data. The new location starts empty.

### Step 3: (Optional) Publish through the reverse proxy

If you set `public_url`, add the DNS and proxy entry for it. See [Configuring an inventory host web service for a reverse proxy](configuring-an-inventory-host-web-service-for-a-reverse-proxy.md). The backend is `http://192.168.2.250:30495`.

---

## 🧩 Custom (Compose) Apps

Use `source: custom` when the app is not in any catalog train, or when the catalog app lacks options you need. Do not set `catalog` or `values`.

```yaml
truenas_apps:
  - name: example-web
    source: custom
    runtime: running
    compose: |
      services:
        web:
          image: nginx:1.27
          restart: unless-stopped
          ports:
            - "8080:80"
          volumes:
            - /mnt/Data/configs/example-web:/usr/share/nginx/html:ro
```

Unlike catalog values, Compose is compared **in both directions** and replaced as a whole on update, so the YAML in the inventory is the complete definition. An app cannot be converted between `catalog` and `custom`.

---

## ▶️ Plan and Apply

1. **Plan** (read-only). Validates locally, then reports the actions for each app:

   ```bash
   ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/deploy_truenas_apps.yml \
     --limit truenas-01 --check --diff -k --ask-vault-pass
   ```

   For a new app, expect `actions: ['create']` and `runtime_state: ABSENT`. App results are redacted while `truenas_no_log` is true. Set it to `false` temporarily only if you need to debug, because it can print secrets.

2. **Apply**:

   ```bash
   ansible-playbook -i inventory/truenas/inventory.ini playbooks/truenas/deploy_truenas_apps.yml \
     --limit truenas-01 -e truenas_apps_mode=apply -k --ask-vault-pass
   ```

   The role waits up to `truenas_apps_job_timeout` (900 s) for the create job and up to `truenas_apps_health_timeout` (180 s) for `RUNNING`. A first install pulls images, so raise the timeouts if your link is slow:

   ```bash
   -e truenas_apps_job_timeout=1800 -e truenas_apps_health_timeout=600
   ```

3. **Verify**:

   ```bash
   midclt call app.query '[["id","=","nexdeck"]]' '{"select":["id","state","version","human_version"]}'
   midclt call app.config nexdeck
   ```

   Then browse to `http://192.168.2.250:30495`.

4. **Run the plan again.** It should report no actions. If it reports `update`, see [Comparison rules](#comparison-rules-to-keep-in-mind).

---

## ⬆️ Upgrading and 🗑️ Removing

**Upgrade.** Find the new catalog version with `midclt call app.upgrade_summary nexdeck '{}'` or from `app.yaml` on GitHub. Check `questions.yaml` for added or renamed keys, then:

```yaml
    catalog:
      version: "1.0.43"        # new catalog version
    allow_upgrade: true
```

Plan, apply, then set `allow_upgrade` back to `false`. Downgrades and versions that `app.upgrade_summary` does not offer are refused.

**Remove.**

```yaml
  - name: nexdeck
    source: catalog
    state: absent
    allow_delete: true
```

The app is deleted, but its images and ix volumes are kept. Remove the volume by hand once you no longer need its data. After the app is gone, you can delete the entry.

---

## 🛠️ Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Each TrueNAS application name must appear exactly once` | Two entries share a `name`, for example a copied Postgres block. | Rename or remove the duplicate. |
| `Check app name ... source, state, runtime ...` | Invalid name, or an unknown top-level key such as `port:` next to `values`. | Move app settings inside `values`. |
| `Catalog apps require catalog.app/train/version ...` | Missing `catalog` field, or `version: latest`. | Pin the exact catalog version as a quoted string. |
| `app.create job ... ended in FAILED` | Middleware rejected `values`, for example `nexdeck.secret_key` shorter than 16 characters, a port already in use, or an invalid enum. | `midclt call core.get_jobs '[["method","=","app.create"]]' '{"order_by":["-id"],"limit":1}'` shows the exact `values.<path>` error. |
| `Existing catalog app/train differs` | `catalog.app` or `train` changed for an existing app. | Delete the app (`allow_delete`) and create it again. |
| `Catalog version change requires allow_upgrade: true` | `catalog.version` differs from the installed version. | Set `allow_upgrade: true`, or pin the installed version. |
| `update` planned on every run | Type mismatch (quoted int), list order, or a key the app normalizes differently. | Compare with `midclt call app.config <name>` and match its types and order. |
| `did not reach RUNNING` | The container crashes or the image pull is slow. | Check the app's logs in the UI, or raise `truenas_apps_health_timeout`. |
| `Configure an Apps storage pool` | No Apps pool is selected in TrueNAS. | Choose one under **Apps → Configuration → Choose Pool**. |

---

## ✅ Checklist for Any New Catalog App

- [ ] Found the app's `train` and **catalog** `version` (not `app_version`)
- [ ] Read `questions.yaml` for that version, and listed all `required` keys with empty defaults
- [ ] Used the app's own key names (`web_port` vs `tcp_port`, `TZ`, app block name)
- [ ] Wrote ints and booleans unquoted
- [ ] Put `private: true` values in `vault.yml` as `vault_truenas_<app>_<key>`
- [ ] Chose a host port that does not conflict with other apps
- [ ] Gave the app a unique `name` in `truenas_apps`
- [ ] Ran the plan, reviewed `actions`, then applied
- [ ] Ran the plan again and confirmed it reports no changes
