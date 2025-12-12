# 🛠️ Role: `minecraft_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Minecraft Server on Ubuntu and Debian systems (https://www.minecraft.net/en-us/download/server).

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `minecraft_setup_version` | `1.21.4` |  |
| `minecraft_setup_port` | `25565` |  |
| `minecraft_setup_download_url` | `https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar` |  |
| `minecraft_setup_java_xmx` | `2048` |  |
| `minecraft_setup_java_xms` | `256` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `minecraft_setup_homedir` | `/minecraft` |  |

## 📑 Tasks
- Create Minecraft server directory
- Download Minecraft server jar
- Accept EULA
- Create server.properties file
- Create systemd service file for Minecraft
- Reload systemd daemon
- Enable Minecraft service
- Start Minecraft service

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `java_setup`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: minecraft_setup
```