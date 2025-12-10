# Role: `entra_id_oauth2`

## 📖 Overview
Configures entra_id settings for oAuth2-enabled sites.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (focal, jammy)

## 🧮 Defaults
- `entra_id_oauth2_secret_expiry_offset_days`: `90` — Number of days to add to current date for secret expiry

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Ensure azure.azcollection required Python modules are installed
- Ensure azure-cli Python module installed
- Filter sites that require OAuth2
- Register Entra ID application for each site
- Calculate secret expiry offset from today
- Login with service principal
- Create client secret for each site
- Build combined secret map
- Build updated list with secrets
- Append each site with injected secret

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: entra_id_oauth2
```