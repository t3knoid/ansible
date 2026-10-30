# 📖 Playbook: deploy_code_server.yml

## 🛠 Purpose
Deploy and configure code-server on target hosts

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`nginx_setup`](../roles/nginx_setup/README.md)
- [`node_exporter_setup`](../roles/node_exporter_setup/README.md)
- [`code_server`](../roles/code_server/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/deploy_code_server.yml
```