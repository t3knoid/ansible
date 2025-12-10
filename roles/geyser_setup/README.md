# 🛠️ Role: `geyser_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Debian | Ubuntu](https://img.shields.io/badge/platforms-Debian%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs and configures GeyserMC on Debian/Ubuntu systems as documented at https://geysermc.org/wiki/geyser/setup/?host=self&platform=standalone


## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `geyser_setup_url` | `https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/standalone` |  |
| `geyser_setup_port` | `19132` |  |
| `geyser_setup_java_xmx` | `1024` |  |
| `geyser_setup_java_xms` | `128` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `geyser_setup_jar` | `Geyser-Standalone.jar` |  |

## 📑 Tasks
- Load Minecraft vars
- Download Geyser jar file
- Create systemd service file for Geyser
- Create Geyser config file
- Reload systemd daemon
- Enable Geyser service
- Start Geyser service

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: geyser_setup
```