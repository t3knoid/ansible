# 📖 Playbook: rproxy/deploy_rproxy.yml

## 🛠 Purpose
Sets up Reverse Proxy on rproxy hosts.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`nginx_setup`](../roles/nginx_setup/README.md)
- [`rproxy_setup`](../roles/rproxy_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/rproxy/deploy_rproxy.yml
```