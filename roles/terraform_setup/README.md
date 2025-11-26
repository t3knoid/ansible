# Role: `terraform_setup`

## 📖 Overview
Installs Terraform

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## 🧮 Defaults
- `terraform_setup_version`: `1.13.5`
- `terraform_setup_home`: `"/usr/local/bin"`
- `terraform_setup_os_arch`: `"linux_amd64"`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Install Terraform dependencies
- Download Terraform
- Unzip terraform.zip
- Make Terraform executable

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: terraform_setup
```