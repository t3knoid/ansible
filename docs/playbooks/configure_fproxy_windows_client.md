# 📖 Playbook: fproxy/configure_fproxy_windows_client.yml

## 🛠 Purpose
Configure Windows client hosts to use the forward proxy for machine environment variables plus WinINet and WinHTTP proxy settings. Targets should be members of the tinyproxy_client group and should not also be members of the linux group. Override tinyproxy_client_proxy_host when the first host in the fproxy group is not the correct reachable address for clients.

## 🔗 Roles Applied
- [`tinyproxy_client`](../roles/tinyproxy_client/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/fproxy/configure_fproxy_windows_client.yml
```