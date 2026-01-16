# 🛠️ Role: `docker_service_deploy`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Ansible role to deploy and manage Docker services using Docker Compose, with configuration templating and optional pre/post deployment hooks. This role is designed to be reusable for various Docker services.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `docker_service_deploy_config_dir` | `""` | Required variables (must be set by the calling role) |
| `docker_service_deploy_backups_dir` | `""` |  |
| `docker_service_deploy_compose_template` | `""` |  |
| `docker_service_deploy_container_name` | `""` |  |
| `docker_service_deploy_config_template` | `""` | Optional config template |
| `docker_service_deploy_config_filename` | `""` |  |
| `docker_service_deploy_pre_config` | `""` | Optional hooks |
| `docker_service_deploy_post_config` | `""` |  |
| `docker_service_deploy_owner` | `"{{ users_list[0].username }}" # Defined in inventory or parent playbook` | Owner defaults |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Stop container
- Run pre-config hook
- Configure service
- Run post-config hook
- Prune unused Docker images
- Pull latest image
- Start container

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: docker_service_deploy
```