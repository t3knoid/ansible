# 🛠️ Role: `users`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: Ubuntu | Debian](https://img.shields.io/badge/platforms-Ubuntu%20|%20Debian-orange.svg)

## 📖 Overview
Provides tasks to manage system users in Ubuntu and Debian.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Ubuntu` (22.04, 24.04)
- Supported on: `Debian` (11, 12)

## ⚙️ Defaults
_No default variables found._

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Create user primary groups
- Add a new user
- Join groups
- Set a user-defined home folder
- Add user to sudoers

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
_No dependencies listed._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: users
```