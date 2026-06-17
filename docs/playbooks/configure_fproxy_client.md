# 📖 Playbook: fproxy/configure_fproxy_client.yml

## 🛠 Purpose
Configure Linux client hosts to use the forward proxy for shell and APT traffic. Targets should be members of both the tinyproxy_client and linux inventory groups. Use configure_fproxy_windows_client.yml for Windows hosts. Override tinyproxy_client_proxy_host when the first host in the fproxy group is not the correct reachable address for clients.

## 🔗 Roles Applied
- [`tinyproxy_client`](../roles/tinyproxy_client/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/fproxy/configure_fproxy_client.yml
```