# Role: `playwright`

## 📖 Overview
Installs playwright.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
_No default variables found in defaults._

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Ensure pip is available
- Install Playwright dependencies
- Install Playwright Python package
- Install Playwright firefox browser binaries

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: playwright
```