# 🖥️ Semaphore UI Setup Guide

This guide explains how to **configure Semaphore UI projects, templates, views, keystores, and schedules** using the `setup_semaphoreui.yml` playbook. It is intended for engineers familiar with Ansible and Semaphore.

> ⚠️ **Important:** The `setup_semaphoreui.yml` playbook **does not install Semaphore UI itself**. Semaphore must already be installed on the target host(s).

---

## 1. Prerequisites

* Semaphore UI installed on Ubuntu VM(s).
* SSH access to the Semaphore host(s).
* Ansible installed on the control node.
* Inventory structured as follows:

```
inventory/
  semaphore/
    inventory.ini
    group_vars/
      semaphore/
        projects.yml
        repositories.yml
        views.yml
        keystores.yml
        templates.yml
        dynamic_templates.yml
        schedules.yml
```

* Each file under `group_vars/semaphore/` defines one aspect of Semaphore configuration.

---

## 2. Define Group Variables

### 2.1 Projects (`projects.yml`)

```yaml
semaphoreui_setup_projects_meta:
  - name: "Home Lab"
    alert_enabled: false
    max_parallel_tasks: 0
```

### 2.2 Repositories (`repositories.yml`)

```yaml
semaphoreui_setup_projects_repositories:
  "Home Lab":
    - name: "Ansible"
      git_url: "https://github.com/t3knoid/ansible.git"
      git_branch: "main"
```

### 2.3 Views (`views.yml`)

```yaml
semaphoreui_setup_projects_views:
  "Home Lab":
    - title: "Linux Checks"
    - title: "Backups"
```

### 2.4 Keystores (`keystores.yml`)

```yaml
semaphoreui_setup_projects_keystores:
  "Home Lab":
    - name: "Semaphore user credentials"
      type: "login_password"
      login_password:
        login: "{{ semaphoreui_setup_semaphore_login }}"
        password: "{{ semaphoreui_setup_semaphore_password }}"
```

### 2.5 Templates (`templates.yml`)

```yaml
semaphoreui_setup_projects_templates:
  "Home Lab":
    - name: "Backup Semaphore Database"
      playbook: "playbooks/semaphoreui/backup_db.yml"
      app: "ansible"
      inventory: "semaphore"
      repository: "Ansible"
      credentials:
        - "Ansible vault password"
      view: "Backups"
```

### 2.6 Dynamic Templates (`dynamic_templates.yml`)

```yaml
dynamic_template_sets:
  "Home Lab":
    - name_prefix: "Check connection to"
      playbook: "playbooks/linux/check_connection.yml"
      inventories:
        - redmine
        - plex
      repository: "Ansible"
      credentials:
        - "Ansible vault password"
      view: "Linux Checks"
```

### 2.7 Scheduled Tasks (`schedules.yml`)

```yaml
semaphoreui_setup_projects_schedules:
  "Home Lab":
    - name: "Nightly Backup"
      template: "Backup Semaphore Database"
      cron: "0 3 * * *"
      enabled: true
```

---

## 3. Run the Playbook

Once the group variables are configured, run the playbook:

```bash
ansible-playbook -k -i inventory/semaphore/inventory.ini setup-semaphore.yml
```

> Notes:
>
> * `-k` prompts for SSH password; omit if using SSH keys.
> * The playbook is **idempotent**; it can be safely re-run.
> * It **only configures Semaphore UI** — it does not perform installation.

---

## 4. Workflow Overview

```
group_vars (projects, repositories, views, keystores, templates, dynamic_templates, schedules)
        |
        v
semaphoreui_setup role (resolves template IDs, applies configuration)
        |
        v
Configured Semaphore UI
```

* **group_vars**: Declarative configuration files maintained by engineers.
* **semaphoreui_setup role**: Reads the variables, generates static/dynamic templates, and creates schedules via Semaphore API.
* **Configured Semaphore UI**: All projects, templates, views, keystores, and scheduled tasks are applied.

---

## 5. Verification

After running the playbook:

1. Log in to Semaphore UI at `https://<semaphore-host>` and verify that:

   * Projects exist
   * Views are created
   * Templates are available
   * Scheduled tasks are configured

2. Optionally, verify via the Semaphore API or CLI:

```bash
semaphore-cli list schedules --project "Home Lab"
```

3. Check Ansible playbook output for skipped or failed tasks.

---

## 6. Tips & Best Practices

* Only modify files under `group_vars/semaphore/`.
* Do **not** edit the `semaphoreui_setup` role code.
* Dynamic templates auto-generate task names using `name_prefix` + inventory names.
