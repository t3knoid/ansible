# 📖 Playbook: vpn/deploy_vpn.yml

## 🛠 Purpose
Deploy the IPsec VPN Docker service on VPN hosts.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`users`](../roles/users/README.md)
- [`docker_setup`](../roles/docker_setup/README.md)
- [`ipsec_vpn_server_setup`](../roles/ipsec_vpn_server_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/vpn/deploy_vpn.yml
```