# Ansible

This repository contains Ansible inventory, roles, and playbooks that I use to manage my homelab network.

The following is a snippet of how the source is structured.

``` bash
├── README.md
├── ansible.cfg
├── docs
├── filter_plugins
├── inventory
│   ├── semaphore
│   │   ├── group_vars
│   │   │   ├── all
│   │   │   │   ├── main.yml
│   │   │   │   └── vault.yml
│   │   │   ├── ansible
│   │   │   │   └── main.yml
│   │   │   ├── pgdb
│   │   │   │   └── main.yml
│   │   │   └── semaphore
│   │   │       └── main.yml
│   │   └── inventory.ini
├── playbooks
│   ├── semaphoreui
│   │   ├── backup_db.yml
│   │   ├── check_semaphore_version.yml
│   │   ├── create_db.yml
│   │   ├── deploy_semaphoreui.yml
│   │   └── setup_semaphoreui.yml
├──roles
│    ├── README.md
│    ├── global
│    ├── README.md
│    ├── defaults
│    │   └── main
│    │   ├── main.yml
│    │   └── vault.yml
│    ├── meta
│    │   └── main.yml
│    ├── tasks
│    │   └── main.yml
│    └── vars
│        └── main.yml
└── scripts
```

These are the main root folders essential to running an Ansible playbook.

| folder | Description           |
|--------|-----------------------|
| docs           | Documentation |
| filter_plugins | Custom filter plugins |
| inventory      | Ansible inventory |
| playbooks      | Ansible playbooks |
| roles          | Ansible roles |
| scripts        | Custom scripts |

## Roles

Roles documentation are available in docs/roles. A README.md file serves as an index to the roles. The role index is also available in roles/README.md. Roles documentation is generated using the [generate_role_docs.py](scripts/generate_role_docs.py). This is automatically executed in GitHub whenever code is commited using GitHub actions. This process is documented in [generate_role_docs.md](docs/scripts/generate_role_docs.md).

## Playbooks

Roles documentation are available in docs/playbooks. A README.md file serves as an index to the playbooks. The playbook index is also available in playbooks/README.md. Playbook documentation is generated using the [generate_playbook_docs.py](scripts/generate_playbook_docs.py). This is automatically executed in GitHub whenever code is commited using GitHub actions. This process is documented in [generate_playbook_docs.md](docs/scripts/generate_playbook_docs.md).

## Inventory

## Filter Plugins

## Scripts
