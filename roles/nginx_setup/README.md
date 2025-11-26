# Role: `nginx_setup`

## 📖 Overview
Installs the nginx service.

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `EL` (7, 8)
- Supported on: `Ubuntu` (bionic, focal)

## 🧮 Defaults
- `nginx_setup_version`: `"1.24.0-2ubuntu7.5"`
- `nginx_setup_site_name`: `"{{ inventory_hostname }}"`
- `nginx_setup_worker_connections`: `768`
- `nginx_setup_homedir`: `/data/nginx`
- `nginx_setup_access_log`: `"{{ nginx_setup_homedir }}/log/access.log"`
- `nginx_setup_conf`: `/etc/nginx/nginx.conf`
- `nginx_setup_certroot`: `/data/certs`
- `nginx_setup_disable_default_site`: `true`
- `nginx_setup_start`: `true`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Update apt cache
- Unhold package versions
- Install nginx
- Hold package versions
- Include config.yml tasks
- Enable nginx

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: nginx_setup
```