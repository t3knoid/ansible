# 📖 Playbook: fproxy/deploy_fproxy.yml

## 🛠 Purpose
Deploy the forward proxy stack on target hosts Runtime assumptions: - Inventory or environment must provide the OpenVPN manual-setup username, password, CA certificate, and remote server when `openvpn_enabled` is true. - The VPN endpoint IP is resolved at deploy time; rerun the playbook if the provider changes that endpoint address.

## 🔗 Roles Applied
- [`tinyproxy_setup`](../roles/tinyproxy_setup/README.md)
- [`openvpn_setup`](../roles/openvpn_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/fproxy/deploy_fproxy.yml
```