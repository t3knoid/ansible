# Role: `vscode_server`

## 📖 Overview
Install and configure Microsoft repository for VSCode.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (20.04, 22.04)

## 🧮 Defaults
- `vscode_server_microsoft_key_url`: `"https://packages.microsoft.com/keys/microsoft.asc"`
- `vscode_server_microsoft_repo_url`: `"https://packages.microsoft.com/repos/code"`
- `vscode_server_vscode_repo_file`: `"/etc/apt/sources.list.d/vscode.list"`
- `vscode_server_keyring_path`: `"/etc/apt/keyrings/packages.microsoft.gpg"`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Install wget and gpg
- Cleanup first
- Download the Microsoft GPG key
- Convert Microsoft GPG key to .gpg format
- Install Microsoft GPG key
- Add Microsoft VSCode repository to sources list
- Clean up the downloaded GPG file
- Install VSCode
- Create script to enable the Code Tunnel Service
- Show instruction on enabling vscode tunnel service

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: vscode_server
```