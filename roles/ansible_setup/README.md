# Role: `ansible_setup`

## 📖 Overview
Provides tasks to install and configure Ansible on a control node.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `ansible_setup_ver`: `10.5.0`
- `ansible_setup_callback_plugins`: ``
- `ansible_setup_workdir`: `"~/ansible/dev"`
- `ansible_setup_config_path`: `"{{ ansible_setup_workdir }}/ansible.cfg"`
- `ansible_setup_git_repository`: `https://github.com/t3knoid/ansible.git`
- `ansible_setup_remote_tmp`: `"~/.ansible/tmp/"`
- `ansible_setup_python_modules`: ``
- `- ansible==12.0.0 # https`: `//pypi.org/project/ansible/`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Create ansible work folder
- Install Ansible Python modules
- Checkout Ansible source code from github
- Create vault password file

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ansible_setup
```