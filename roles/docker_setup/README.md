# 🛠️ Role: `docker_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs Docker and Docker Compose on Debian/Ubuntu systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `docker_setup_containerd_version` | `1.7.24-1` |  |
| `docker_setup_docker_ce_version` | `27.3.1-1` |  |
| `docker_setup_buildx_plugin_version` | `0.17.1-1` |  |
| `docker_setup_docker_compose_plugin_version` | `2.29.7-1` |  |
| `docker_setup_arch` | `amd64` |  |
| `docker_setup_distro` | `noble` |  |
| `docker_setup_download_root` | `"https://download.docker.com/linux/ubuntu/dists"` |  |
| `docker_setup_packages` | `` |  |
| `docker_setup_compose_version` | `v2.31.0` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Uninstall conflicting packages
- Install Docker packages
- Start Docker service
- Test Docker service
- Show Docker test output on failure
- Docker failure
- Stop Test Docker container
- Remove Test Docker container
- Remove Test Docker image
- Install docker-compose

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: docker_setup
```