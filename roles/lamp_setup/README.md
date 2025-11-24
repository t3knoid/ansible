# Role: `lamp_setup`

## 📖 Overview
Install and configure LAMP on Debian/Ubuntu.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## 🧮 Defaults
- `lamp_setup_packages`: ``
- `- mariadb-server=1`: `10.11.13-0ubuntu0.24.04.1`
- `- php=2`: `8.3+93ubuntu2`
- `- php-intl=2`: `8.3+93ubuntu2`
- `- php-mysql=2`: `8.3+93ubuntu2`
- `- libapache2-mod-php=2`: `8.3+93ubuntu2`
- `- php-xml=2`: `8.3+93ubuntu2`
- `- php-mbstring=2`: `8.3+93ubuntu2`
- `- php-curl=2`: `8.3+93ubuntu2`
- `- php-ldap=2`: `8.3+93ubuntu2`
- `- imagemagick=8`: `6.9.12.98+dfsg1-5.2build2`
- `- php-gd=2`: `8.3+93ubuntu2`
- `- php-bcmath=2`: `8.3+93ubuntu2`
- `- git=1`: `2.43.0-1ubuntu7.3`
- `lamp_setup_mysql_socket`: `/run/mysqld/mysqld.sock`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Get installed packages
- Unhold package versions if it is installed
- Install lamp packages
- Hold package versions
- Check if MySQL root password is already set
- Setting root password for mysql server

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: lamp_setup
```