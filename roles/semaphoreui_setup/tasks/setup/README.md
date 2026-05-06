# Semaphore UI Setup Tasks

This directory contains the task files used by the Semaphore UI setup workflow that is invoked by [playbooks/semaphoreui/setup_semaphoreui.yml](../../../../playbooks/semaphoreui/setup_semaphoreui.yml).

The playbook does not install Semaphore UI. It assumes Semaphore has already been installed and configured enough for API access, then reconciles projects, inventories, credentials, repositories, templates, and schedules using the Semaphore API.

## Entry Point

The playbook [playbooks/semaphoreui/setup_semaphoreui.yml](../../../../playbooks/semaphoreui/setup_semaphoreui.yml) runs the `semaphoreui_setup` role with `tasks_from: setup/main.yml`.

High-level flow:

1. Target the `semaphore` hosts.
2. Gather facts and run with `become: true`.
3. Import [main.yml](main.yml).
4. Use the Semaphore API to reconcile the configured state.

## Prerequisites

Before running the setup playbook, the following must already be true:

1. Semaphore UI is installed and reachable on `semaphoreui_setup_api_base`.
2. The Semaphore admin password file exists at `{{ semaphoreui_setup_homedir }}/.admin`.
3. Database and core config values for the `semaphoreui_setup` role are already in place.
4. The Semaphore project data files under [inventory/semaphore/group_vars/semaphore](../../../../inventory/semaphore/group_vars/semaphore) are populated with the projects, repositories, keystores, views, templates, dynamic templates, and schedules the role should apply.

The admin login and API token bootstrap is handled by [create_api_token.yml](create_api_token.yml).

## Configuration Inputs

The setup flow assembles project state from variables exposed by the role and inventory data.

Important inputs include:

1. `semaphoreui_setup_api_base`
2. `semaphoreui_setup_projects_meta`
3. `semaphoreui_setup_projects_repositories`
4. `semaphoreui_setup_projects_keystores`
5. `semaphoreui_setup_projects_views`
6. `semaphoreui_setup_projects_templates`
7. `semaphoreui_setup_projects_schedules`
8. `dynamic_template_sets`

Static defaults for the role live in [roles/semaphoreui_setup/defaults/main/main.yml](../../defaults/main/main.yml).

## Where the Setup Data Comes From

The setup playbook does not hardcode the Semaphore project model. It reads that model from inventory variables, primarily from the files in [inventory/semaphore/group_vars/semaphore](../../../../inventory/semaphore/group_vars/semaphore).

For the `semaphore` inventory, the main data sources are:

1. [projects.yml](../../../../inventory/semaphore/group_vars/semaphore/projects.yml): defines `semaphoreui_setup_projects_meta`.
2. [repositories.yml](../../../../inventory/semaphore/group_vars/semaphore/repositories.yml): defines `semaphoreui_setup_projects_repositories`.
3. [keystores.yml](../../../../inventory/semaphore/group_vars/semaphore/keystores.yml): defines `semaphoreui_setup_projects_keystores`.
4. [views.yml](../../../../inventory/semaphore/group_vars/semaphore/views.yml): defines `semaphoreui_setup_projects_views`.
5. [templates.yml](../../../../inventory/semaphore/group_vars/semaphore/templates.yml): defines `semaphoreui_setup_projects_templates`.
6. [dynamic_templates.yml](../../../../inventory/semaphore/group_vars/semaphore/dynamic_templates.yml): defines `dynamic_template_sets`.
7. [schedules.yml](../../../../inventory/semaphore/group_vars/semaphore/schedules.yml): defines `semaphoreui_setup_projects_schedules`.
8. [main.yml](../../../../inventory/semaphore/group_vars/semaphore/main.yml): carries the remaining Semaphore host and role variables used by the setup workflow.

The role then combines those separate variable files into a single in-memory structure in [main.yml](main.yml) before calling the API.

## What `main.yml` Does

The orchestration file [main.yml](main.yml) performs the following steps:

1. Discover inventory files under `inventory/` using the `find_inventory_files` filter.
2. Build `semaphoreui_setup_inventories` objects for each discovered `inventory.ini`.
3. Bind generated inventories to `Ansible user credentials`.
4. Create an admin API token if one is not already present.
5. Enumerate existing Semaphore users.
6. Build a normalized in-memory project definition from the project data files under [inventory/semaphore/group_vars/semaphore](../../../../inventory/semaphore/group_vars/semaphore).
7. Expand dynamic template sets with `extract_templates_for_project`.
8. Merge static and dynamic templates into the final `semaphoreui_setup_projects` structure.
9. Call [setup_projects.yml](setup_projects.yml) to reconcile each project.
10. Expire the temporary API token when finished.

## Dynamic Templates

Dynamic templates exist to avoid repeating the same template definition over and over when multiple inventories should run the same playbook.

Instead of manually defining one static Semaphore template per inventory, you define one shared template pattern in `dynamic_template_sets` and list the inventories it applies to. The setup role then expands that single definition into multiple concrete Semaphore templates, one per inventory.

This is useful when:

1. Several inventories should run the same playbook.
2. The only meaningful difference between the resulting templates is the target inventory.
3. You want to keep the inventory-specific template list short and easier to maintain.

For example, this dynamic template definition:

```yaml
- name_prefix: "Deploy security updates to"
	playbook: "playbooks/linux/deploy_updates.yml"
	inventories:
		- plex
		- ombi
		- services
```

is expanded into separate Semaphore templates such as:

1. `Deploy security updates to plex`
2. `Deploy security updates to ombi`
3. `Deploy security updates to services`

Each generated template points to the same playbook, `playbooks/linux/deploy_updates.yml`, but uses a different inventory.

Dynamic templates are appended during the `setup/main.yml` workflow. They are expanded per inventory and merged into the project's `templates` list before any API calls create or update task templates.

Relevant files:

1. [main.yml](main.yml)
2. [filter_plugins/extract_templates_for_projects.py](../../../../filter_plugins/extract_templates_for_projects.py)
3. [docs/filters/extract_templates_for_projects.md](../../../../docs/filters/extract_templates_for_projects.md)

Typical source data for dynamic templates is stored in inventory variables such as [inventory/semaphore/group_vars/semaphore/dynamic_templates.yml](../../../../inventory/semaphore/group_vars/semaphore/dynamic_templates.yml).

## Reconciliation Order Per Project

The file [setup_project.yml](setup_project.yml) drives the per-project reconciliation order.

For each project, it:

1. Loads the current project definition from `semaphoreui_setup_projects`.
2. Reads current environments, keys, repositories, inventories, views, templates, and schedules from the Semaphore API.
3. Reconciles schedules.
4. Reconciles views.
5. Re-reads views.
6. Reconciles keystores.
7. Re-reads keys.
8. Reconciles repositories.
9. Re-reads repositories.
10. Reconciles inventories.
11. Re-reads inventories.
12. Reconciles task templates.

This ordering matters because later resources depend on earlier ones. For example:

1. Inventories depend on keystore IDs.
2. Templates depend on repository, inventory, view, environment, and vault references.
3. Schedules depend on templates that already exist in Semaphore.

## Task File Responsibilities

Each file in this directory has a narrow API-oriented responsibility:

1. [create_api_token.yml](create_api_token.yml): logs in as admin, creates a temporary token, logs out.
2. [enum_users.yml](enum_users.yml): enumerates existing Semaphore users.
3. [setup_projects.yml](setup_projects.yml): creates missing projects, then maps project names to IDs.
4. [setup_project.yml](setup_project.yml): orchestrates reconciliation of a single project.
5. [setup_views.yml](setup_views.yml): reconciles project views.
6. [setup_keystores.yml](setup_keystores.yml): reconciles project access keys and updates existing managed keys when login data changes.
7. [setup_repositories.yml](setup_repositories.yml): reconciles project repositories.
8. [setup_inventories.yml](setup_inventories.yml): loops inventories for a project.
9. [setup_inventory.yml](setup_inventory.yml): reconciles a single inventory and updates the bound SSH credential when needed.
10. [setup_templates.yml](setup_templates.yml): loops task templates for a project.
11. [setup_template.yml](setup_template.yml): creates a single task template with resolved repository, inventory, view, environment, and vault IDs.
12. [setup_schedules.yml](setup_schedules.yml): reconciles schedules.

## Credentials and Inventory Behavior

Generated inventories are built automatically from the repository's Ansible inventory files and are associated with `Ansible user credentials`.

The current behavior is:

1. New inventories are created when missing.
2. Existing managed inventories are updated when their path, type, or SSH credential binding changes.
3. Existing managed keystores are updated when the configured login changes.

This keeps the Semaphore-side configuration aligned with the role variables instead of relying on manual UI edits.

## How to Add a New Keystore

To add a new keystore to Semaphore UI through this playbook, update the Semaphore inventory data and rerun the setup playbook.

User workflow:

1. Open [inventory/semaphore/group_vars/semaphore/keystores.yml](../../../../inventory/semaphore/group_vars/semaphore/keystores.yml).
2. Find the project entry in `semaphoreui_setup_projects_keystores` that should own the new keystore.
3. Add a new object to that project's keystore list.
4. Set the keystore `name`, `type`, and the fields required by that type.
5. Run [playbooks/semaphoreui/setup_semaphoreui.yml](../../../../playbooks/semaphoreui/setup_semaphoreui.yml) again.

Example for a `login_password` keystore:

```yaml
semaphoreui_setup_projects_keystores:
	"Home Lab":
		- name: "My new SSH credentials"
			type: "login_password"
			login_password:
				login: "ansible"
				password: "{{ vault_my_new_password }}"
```

You can add other supported key types in the same file, such as:

1. `login_password`
2. `ssh`
3. `none`

What happens when you rerun the playbook:

1. The role reads [keystores.yml](../../../../inventory/semaphore/group_vars/semaphore/keystores.yml).
2. It compares the desired keystore names to the existing Semaphore keystores for that project.
3. If the keystore does not exist, it is created.
4. If a keystore with the same name already exists, the role may update it when the managed login or key type has changed.

Current reconciliation behavior for keystores:

1. Missing keystores are created.
2. Existing keystores with the same name are updated when the managed login or key type changes.
3. Existing keystores are not deleted by this role.

Implementation details are in [setup_keystores.yml](setup_keystores.yml), but the user-facing change is simply: update [keystores.yml](../../../../inventory/semaphore/group_vars/semaphore/keystores.yml) and rerun the setup playbook.

## How a New Template Is Added

Templates enter the workflow from either static project configuration or dynamic template expansion.

A new template can come from:

1. `semaphoreui_setup_projects_templates` for static templates.
2. `dynamic_template_sets` expanded by `extract_templates_for_project` for generated templates.

The add flow is:

1. [main.yml](main.yml) builds the final `semaphoreui_setup_projects` structure and merges static and dynamic templates into each project's `templates` list.
2. [setup_project.yml](setup_project.yml) fetches the current templates, inventories, repositories, views, keys, and environments for the project.
3. [setup_templates.yml](setup_templates.yml) loops through each desired template and includes [setup_template.yml](setup_template.yml).
4. [setup_template.yml](setup_template.yml) resolves the IDs for the referenced repository, inventory, view, and environment by name.
5. It converts each credential name in the template into a Semaphore `vaults` entry using the existing project keystores.
6. It removes non-API helper fields such as `credentials`, `inventory`, `view`, `repository`, and `environment` from the template definition to create the API payload.
7. If a template with the same name does not already exist in the project, the role sends a `POST` request to `/project/{project_id}/templates`.

For a template to be created successfully, the referenced resources must already exist in Semaphore for that project:

1. The repository name must resolve to an existing repository.
2. The inventory name must resolve to an existing inventory.
3. The view title must resolve to an existing view when one is specified.
4. The environment name must resolve to an existing environment when one is specified.
5. Each credential listed in `credentials` must match an existing keystore name.

Current reconciliation behavior for templates:

1. Missing templates are created.
2. Existing templates are detected by name and skipped.
3. Existing templates are not currently updated in place by this role.

This means that changing the definition of an already-created template in inventory variables does not automatically modify the template in Semaphore unless the role is extended with template update logic.

Relevant files:

1. [setup_templates.yml](setup_templates.yml)
2. [setup_template.yml](setup_template.yml)
3. [main.yml](main.yml)

## Running the Playbook

Typical invocation:

```bash
ansible-playbook -i inventory/semaphore/inventory.ini playbooks/semaphoreui/setup_semaphoreui.yml
```

If Vault or SSH prompts are required in your environment, pass the usual Ansible flags such as `-K`, `-k`, or `--ask-vault-pass` as needed.

## Notes

1. This workflow is API-driven and is intended to be rerunnable.
2. The role is not purely create-only; several setup tasks now reconcile existing Semaphore objects.
3. If a playbook run fails after token creation but before cleanup, an API token may remain active until it is expired.
