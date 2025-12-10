# 🛠️ Role: `tautulli_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures an Tautulli Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/tautulli).


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `tautulli_setup_version` | `2.16.0` |  |
| `tautulli_setup_config_dir` | `"/config"` |  |
| `tautulli_setup_port` | `8181` |  |
| `tautulli_setup_host` | `"http://localhost:8181"` | tautulli_apikey |
| `tautulli_setup_backup_dir_final` | `"/nfs/backups/tautulli"` |  |
| `tautulli_setup_backup_dir_original` | `"{{ tautulli_setup_config_dir }}/backups"` |  |

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Verify config folder exists
- Fail if config folder does not exists
- Copy docker-compose.yml to target machine
- Make sure docker service account has access to config dir
- Stop Docker Container
- Prune unused Docker images
- Remove all images
- Pull latest image
- Run Docker Container

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `global`
- `users`
- `docker_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: tautulli_setup
```