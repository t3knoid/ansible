# 📖 Playbook: oauth2_proxy/deploy_oauth2_proxy.yml

## 🛠 Purpose
Deploy OAuth2 Proxy with Entra ID as the identity provider

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`entra_id_oauth2`](../roles/entra_id_oauth2/README.md)
- [`redis_setup`](../roles/redis_setup/README.md)
- [`oauth2_proxy_setup`](../roles/oauth2_proxy_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/oauth2_proxy/deploy_oauth2_proxy.yml
```