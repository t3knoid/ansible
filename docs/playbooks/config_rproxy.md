# 📖 Playbook: rproxy/config_rproxy.yml

## 🛠 Purpose
Configures Reverse Proxy for specified sites. rproxy_setup_sites variable should be defined in the inventory or host_vars.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`nginx_setup`](../roles/nginx_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/rproxy/config_rproxy.yml
```