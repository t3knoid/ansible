# 🛠️ Role: `aws_cli`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures AWS CLI.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `aws_cli_user` | `terraform-svc` |  |
| `aws_cli_region` | `"us-west-2"` |  |
| `aws_cli_output` | `"json"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Install required packages
- Download AWS CLI v2
- Unzip AWS CLI v2
- Install AWS CLI v2
- Clean up AWS CLI v2 installer
- Clean up extracted AWS CLI installer
- Configure AWS CLI

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: aws_cli
```