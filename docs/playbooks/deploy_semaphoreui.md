# 📖 Playbook: semaphoreui/deploy_semaphoreui.yml

## 🛠 Purpose
Installs Semaphore UI application on semaphore hosts.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`sshpass`](../roles/sshpass/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`azure_cli_setup`](../roles/azure_cli_setup/README.md)
- [`entra_id_oauth2`](../roles/entra_id_oauth2/README.md)
- [`semaphoreui_setup`](../roles/semaphoreui_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/semaphoreui/deploy_semaphoreui.yml
```