# 🛠️ Role: `bedrock_setup`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Installs Minecraft Bedrock Server on Linux systems.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `bedrock_setup_version` | `1.21.62.01` |  |
| `bedrock_setup_download_url` | `https://www.minecraft.net/bedrockdedicatedserver/bin-linux` |  |
| `bedrock_setup_download_archive` | `bedrock-server-{{ bedrock_setup_version }}.zip` |  |
| `bedrock_setup_server_props` | `` |  |
| `- { key` | `'server-port', value: '19132' }` |  |
| `- { key` | `'gamemode', value: 'creative' }` |  |
| `- { key` | `'online-mode', value: 'true' }` |  |
| `- { key` | `'server-name', value: "Dad's Minecraft Server" }` |  |
| `- { key` | `'max-players', value: '10' }` |  |
| `- { key` | `'difficulty', value: 'easy' }` |  |
| `- { key` | `'content-log-file-enabled', value: 'false' }` |  |
| `- { key` | `'allow-cheats', value: 'false' }` |  |
| `- { key` | `'default-player-permission-level', value: 'visitor' }` |  |
| `- { key` | `'allow-cheats', value: 'false' }` |  |
| `- { key` | `'allow-list', value: 'false' }` |  |
| `- { key` | `'enable-lan-visibility', value: 'true' }` |  |
| `- { key` | `'view-distance', value: '32' }` |  |
| `- { key` | `'tick-distance', value: '4' }` |  |
| `- { key` | `'player-idle-timeout', value: '30' }` |  |
| `- { key` | `'max-threads', value: '8' }` |  |
| `- { key` | `'level-required', value: 'false' }` |  |
| `- { key` | `'texturepack-required', value: 'false' }` |  |
| `- { key` | `'level-name', value: "{{ (bedrock_setup_worlds` |  |

## 📦 Vars
| Variable | Default Value | Description |
|----------|---------------|-------------|
| `bedrock_setup_homedir` | `/minecraft` |  |
| `bedrock_setup_worlddir` | `"{{ bedrock_setup_homedir }}/worlds"` |  |
| `bedrock_setup_worlds` | `` |  |
| `- name` | `"EuroCraft" # https://www.minecraftmaps.com/50755-eurocraft` |  |
| `src` | `"EuroCraft-Bedrock-1.0.mcworld"` |  |
| `dest` | `"{{ bedrock_setup_worlddir }}/EuroCraft"` |  |
| `active` | `false` |  |
| `- name` | `"Horror Hunt" # https://mcpedl.com/horror-hunt/` |  |
| `src` | `"HorrorHunt_v1.0.4.mcworld"` |  |
| `dest` | `"{{ bedrock_setup_worlddir }}/HorrorHunt"` |  |
| `active` | `false` |  |

## 📑 Tasks
- Create Bedrock server directory
- Download Bedrock server archive
- Set bedrock_server executable
- Configure Bedrock server.properties
- Create permissions.json file
- Create systemd service file for Bedrock
- Copy server icon
- Ensure worlds directory exists
- Deploy all worlds
- Enable Bedrock service
- Flush handlers to ensure service is restarted before checking version
- Get Bedrock start timestamp
- Extract Bedrock version from latest journal entries
- Parse version number
- Compare extracted version to expected setup version

## 🔔 Handlers
- Reload systemd daemon
- Restart Bedrock service

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: bedrock_setup
```