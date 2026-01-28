# 🛠️ Role: `playwright`

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Ansible >= 2.9](https://img.shields.io/badge/ansible-%3E%3D%202.9-green.svg)
![Platforms: EL | Ubuntu](https://img.shields.io/badge/platforms-EL%20|%20Ubuntu-orange.svg)

## 📖 Overview
Installs playwright.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## ⚙️ Defaults
_No default variables found._

## 📦 Vars
_No constant variables found._

## 📑 Tasks
- Ensure pip is available
- Install Playwright Python package
- Install Playwright dependencies
- Install Playwright firefox browser binaries

## 🔔 Handlers
_No handlers defined._

## 🔗 Dependencies
- `python3`

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: playwright
```