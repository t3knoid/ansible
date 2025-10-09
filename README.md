# Ansible

This repository contains Ansible inventory, roles, and playbooks that I use to manage my homelab network.

The following is a snippet of how the source is structured.

``` bash
├── README.md
├── ansible.cfg
├── filter_plugins
├── generate_role_docs.py
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
└── roles
    ├── README.md
    ├── global
    ├── README.md
    ├── defaults
    │   └── main
    │   ├── main.yml
    │   └── vault.yml
    ├── meta
    │   └── main.yml
    ├── tasks
    │   └── main.yml
    └── vars
        └── main.yml
```

These are the main root folders essential to running an Ansible playbook.

- filter_plugins
- inventory
- playbooks
- roles

## Roles

Roles documentation are available in each role folder inside a README.md file. The README.md file is automatically generated using the [generate_role_docs.py](generate_role_docs.py) script located in the root of the repository.

An index of the roles is listed inside the root of the roles/ folder. It is aptly named [README.md](roles/README.md) as well.

The role documentation is generated from metadata information inside each role's meta/main.yml file. Here is an example using the ansible_setup role's metadata file.

``` bash
---
galaxy_info:
  role_name: global
  author: Francis Refol
  description: Provides tasks to install and configure Ansible on a control node.
  license: MIT
  min_ansible_version: "2.9"
  platforms:
    - name: EL
      versions:
        - "7"
        - "8"
    - name: Ubuntu
      versions:
        - bionic
        - focal
```

Along with this information, the script also extracts all default and static variables in the role. A comment that precedes a variable is assumed to be a comment related to the variable.

Execute the generate_role_docs.py to generate the role documentation.

``` bash
python generate_role_docs.py 
```

## Inventory

TBD

## Playbooks

TBD

## Filter Plugins

TBD