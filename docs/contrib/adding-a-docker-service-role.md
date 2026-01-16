# 🐳 Contributor Guide: Adding a Docker Service Role

This role provides a **shared, reusable deployment workflow** for Docker‑based services in the homelab. It eliminates duplication across service roles by centralizing common tasks such as stopping containers, preparing configuration directories, templating files, pruning images, pulling updates, and starting containers.

Service‑specific roles (e.g., Sonarr, Sabnzbd, Radarr) import this role and supply only the variables and optional hooks they need.

---

## 📦 **What This Role Does**

The role implements the following workflow:

1. **Stop the existing container**
   Uses pure Docker CLI to ensure compatibility even when docker‑compose is not available.

2. **Run optional pre‑config hook**
   Allows a service to perform custom logic before configuration (e.g., Sabnzbd domain lookup).

3. **Configure the service**
   - Creates config and backup directories
   - Optionally templates a service config file
   - Always templates the docker‑compose file
   - Ensures correct ownership and permissions

4. **Run optional post‑config hook**
   For services that need additional steps after templating.

5. **Prune unused Docker images**
   Removes dangling images and optionally all images if desired.

6. **Pull the latest image**
   Uses docker‑compose to fetch updated images.

7. **Start the container**
   Brings the service up using docker‑compose.

This workflow is consistent across all services, ensuring predictable behavior and reducing maintenance overhead.

---

## 🧩 **Required Variables**

Each service role must define the following:

| Variable | Description |
|---------|-------------|
| `docker_service_deploy_container_name` | Name of the Docker container (e.g., `"sonarr"`) |
| `docker_service_deploy_config_dir` | Path to the service’s config directory |
| `docker_service_deploy_backups_dir` | Path to the service’s backup directory |
| `docker_service_deploy_compose_template` | Jinja2 template for `docker-compose.yml` |

Example:

```yaml
docker_service_deploy_container_name: "sonarr"
docker_service_deploy_config_dir: "{{ sonarr_setup_config_dir }}"
docker_service_deploy_backups_dir: "{{ sonarr_setup_backups_dir }}"
docker_service_deploy_compose_template: "docker-compose.yml.j2"
```

---

## 📝 **Optional Variables**

These allow services to customize behavior without modifying the shared role.

### **Optional config templates**

Some services have one or more standalone configuration files (e.g., `config.xml`, `sabnzbd.ini`, `database.json`). Others rely entirely on environment variables or the docker‑compose file.

To support all cases, the role accepts **a list of config templates**, each with its own source, destination filename, and optional mode.

| Variable | Description |
|----------|-------------|
| `docker_service_deploy_config_templates` | A list of config templates to render into the service’s config directory (optional) |

Each item in the list supports:

- `src` — the Jinja2 template filename
- `dest` — the output filename
- `mode` — optional file mode (defaults to `0640`)

Example:

```yaml
docker_service_deploy_config_templates:
  - src: "database.json.j2"
    dest: "database.json"
    mode: "0600"
  - src: "settings.json.j2"
    dest: "settings.json"
```

If the list is omitted or empty, the config‑templating step is skipped.

---

### **Optional hooks**

Hooks allow services to inject custom logic before or after configuration.

| Variable | Description |
|----------|-------------|
| `docker_service_deploy_pre_config` | Task file to run before configuration |
| `docker_service_deploy_post_config` | Task file to run after configuration |

Hooks are only executed when set to a truthy value.

Example:

```yaml
docker_service_deploy_pre_config: pre_config.yml
```

---

### **Owner**

Defaults to the first user in `users_list`, but can be overridden:

```yaml
docker_service_deploy_owner: "media"
```

---

## 🧱 **Role Structure**

```
roles/docker_service_deploy/
├── defaults/
│   └── main.yml
├── tasks/
│   ├── main.yml
│   ├── stop.yml
│   ├── config.yml
│   ├── prune.yml
│   ├── pull.yml
│   └── start.yml
```

Each file is small, focused, and easy to override or extend.

---

## 🚀 **How to Use This Role in a Service Role**

### **Simple service (Sonarr)**

```yaml
- import_role:
    name: docker_service_deploy
  vars:
    docker_service_deploy_container_name: "sonarr"
    docker_service_deploy_config_dir: "{{ sonarr_setup_config_dir }}"
    docker_service_deploy_backups_dir: "{{ sonarr_setup_backups_dir }}"
    docker_service_deploy_config_template: "config.xml.j2"
    docker_service_deploy_config_filename: "config.xml"
    docker_service_deploy_compose_template: "docker-compose.yml.j2"
```

---

### **Service with custom logic (Sabnzbd)**

`tasks/pre_config.yml`:

```yaml
- name: Determine Sabnzbd domain
  set_fact:
    sabnzbd_setup_domain_name: >-
      {{ rproxy_setup_sites
        | selectattr('server_name', 'defined')
        | selectattr('server_name', 'search', '^sabnzbd')
        | map(attribute='server_name')
        | first
        | default('', true) }}
```

`tasks/main.yml`:

```yaml
- import_role:
    name: docker_service_deploy
  vars:
    docker_service_deploy_container_name: "sabnzbd"
    docker_service_deploy_pre_config: pre_config.yml
    docker_service_deploy_config_dir: "{{ sabnzbd_setup_config_dir }}"
    docker_service_deploy_backups_dir: "{{ sabnzbd_setup_backups_dir }}"
    docker_service_deploy_config_template: "sabnzbd.ini.j2"
    docker_service_deploy_config_filename: "sabnzbd.ini"
    docker_service_deploy_compose_template: "docker-compose.yml.j2"
```

---

## 🧼 **Contributor Expectations**

- Do **not** duplicate logic already provided by this role.
- Use hooks (`pre_config`, `post_config`) for service‑specific behavior.
- Keep service roles declarative: set variables, provide templates, and let this role handle the workflow.
- Avoid modifying this role unless the change benefits *all* services.
- When adding a new service, follow the examples above for consistency.

---

## 🧭 **Design Philosophy**

This role exists to:

- enforce consistency
- reduce duplication
- simplify onboarding
- make service roles thin and readable
- centralize Docker deployment logic
- support optional complexity without clutter

It reflects the homelab’s broader principles: **modular, predictable, DRY, and contributor‑friendly**.
