# 📖 Playbook: semaphoreui/deploy_semaphoreui.yml

## 🛠 Purpose
Installs Semaphore UI application on semaphore hosts. - name: Deploy postgresql ansible.builtin.import_playbook: ../postgresql/deploy_postgresql.yml - name: Create the SemaphoreUI database ansible.builtin.import_playbook: create_db.yml - name: Install Ansible ansible.builtin.import_playbook: ../ansible/deploy_ansible.yml

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/semaphoreui/deploy_semaphoreui.yml
```