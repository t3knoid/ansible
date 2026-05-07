# 📖 Playbook: services/deploy_lidarr.yml

## 🛠 Purpose
Installs Lidarr application. - name: Create Lidarr postgresql database import_playbook: create_lidarr_db.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`lidarr_setup`](../roles/lidarr_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/services/deploy_lidarr.yml
```