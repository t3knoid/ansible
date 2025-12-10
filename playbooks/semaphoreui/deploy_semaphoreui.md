# 📖 Playbook: semaphoreui/deploy_semaphoreui.yml

## 🛠 Purpose
Installs Semaphore UI application on semaphore hosts.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`sshpass`](../roles/sshpass/README.md)
- [`autofs`](../roles/autofs/README.md)
- [`semaphoreui_setup`](../roles/semaphoreui_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/semaphoreui/deploy_semaphoreui.yml
```