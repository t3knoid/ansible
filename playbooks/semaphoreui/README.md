# 📚 Playbooks in `semaphoreui`

| Playbook | Purpose |
|----------|---------|
| [`backup_db.yml`](backup_db.md) | Backup Semaphore UI database to NFS share. |
| [`check_semaphore_version.yml`](check_semaphore_version.md) | Check the latest version of SemaphoreUI available. |
| [`create_db.yml`](create_db.md) | Create PostgreSQL database for Semaphore UI application. |
| [`deploy_semaphoreui.yml`](deploy_semaphoreui.md) | Installs Semaphore UI application on semaphore hosts. |
| [`setup_semaphoreui.yml`](setup_semaphoreui.md) | Sets up Semaphore UI application on semaphore hosts. It configures the Semaphore using the values in the semaphoreui_setup_projects variable. This playbook assumes that Semaphore UI has been installed. |