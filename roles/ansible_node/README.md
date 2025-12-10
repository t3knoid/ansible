# Role: `ansible_node`

## 📖 Overview
Configures a node to be used as an Ansible control node.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `ansible_node_custom_sudo_users`: ``
- `ansible_node_remote_tmp`: `"/tmp/.ansible/$USER"`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Ensure ansible group exists
- Store USER value, set to undefined if not defined
- Store SUDO_USER value
- Add current_user to ansible group, if undefined, use SUDO_USER value instead
- Add custom user list to ansible group
- Ensure sudoers.d directory exists
- Add 'ansible' group to sudoers with NOPASSWD
- Ensure remote temp directory exists

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: ansible_node
```