# 📚 Playbook Index

## 📂 Playbooks in root `playbooks/`

| Playbook | Purpose |
|----------|---------|
| [`deploy_code_server.yml`](../docs/playbooks/deploy_code_server.md) | Deploy and configure code-server on target hosts |
| [`deploy_vscode_server.yml`](../docs/playbooks/deploy_vscode_server.md) | Deploy and configure VSCode Server on target hosts |
| [`disable_code_server.yml`](../docs/playbooks/disable_code_server.md) | Stop and disable code-server on target hosts |
| [`enable_code_server.yml`](../docs/playbooks/enable_code_server.md) | Start and enable code-server on target hosts |
| [`provision_vm.yml`](../docs/playbooks/provision_vm.md) | Provision a new VM and prepare it as an Ansible node |

## 📂 Playbooks in subfolders

| Playbook Path | Purpose |
|---------------|---------|
| [`ad/join_domain.yml`](../docs/playbooks/join_domain.md) | Join hosts to an Active Directory domain |
| [`ad/leave_domain.yml`](../docs/playbooks/leave_domain.md) | Remove hosts from an Active Directory domain |
| [`ansible/deploy_ansible.yml`](../docs/playbooks/deploy_ansible.md) | Deploy and configure Ansible on the control node |
| [`ansible/install_python3_modules.yml`](../docs/playbooks/install_python3_modules.md) | Install required Python 3 modules for Ansible operation |
| [`ansible/prep_ansible_node.yml`](../docs/playbooks/prep_ansible_node.md) | Prepare nodes to be managed by Ansible |
| [`ansible/remove_python3_modules.yml`](../docs/playbooks/remove_python3_modules.md) | Remove Python 3 modules no longer needed for Ansible operation |
| [`aws/deploy_aws_cli.yml`](../docs/playbooks/deploy_aws_cli.md) | Deploy AWS CLI on target hosts |
| [`azure/deploy_azure_cli.yml`](../docs/playbooks/deploy_azure_cli.md) | Deploy Azure CLI on target hosts |
| [`azure/deploy_azure_ps.yml`](../docs/playbooks/deploy_azure_ps.md) | Deploy Azure Powershell on the Ansible control node |
| [`azure/entra_id_for_oauth2.yml`](../docs/playbooks/entra_id_for_oauth2.md) | Configure Entra ID applications for OAuth2 authentication |
| [`baremetal/reboot.yml`](../docs/playbooks/reboot.md) | Reboot baremetal machines using the vms role's reboot tasks |
| [`baremetal/shutdown.yml`](../docs/playbooks/shutdown.md) | Unconditionally shut down baremetal machine with all defaults |
| [`certbot/deploy_certbot.yml`](../docs/playbooks/deploy_certbot.md) | Deploy Certbot on target hosts |
| [`certs/distribute_pve_certs.yml`](../docs/playbooks/distribute_pve_certs.md) | Distribute web certificates from cert staging host to Proxmox nodes |
| [`certs/generate_all_certs.yml`](../docs/playbooks/generate_all_certs.md) | Generate Let’s Encrypt certbot certificates for every domain |
| [`certs/generate_certs.yml`](../docs/playbooks/generate_certs.md) | Generate Let’s Encrypt certbot certificates on the cert staging host |
| [`certs/stage_all_certs.yml`](../docs/playbooks/stage_all_certs.md) | Stage all certificates on the cert staging host in preparation for use by reverse proxy and other services |
| [`certs/stage_certs.yml`](../docs/playbooks/stage_certs.md) | Stage certificates on the cert staging host in preparation for use by reverse proxy and other services |
| [`dns/add_cname_entry.yml`](../docs/playbooks/add_cname_entry.md) | Add CNAME entries to Pi-hole DNS server |
| [`dns/add_dns_entry.yml`](../docs/playbooks/add_dns_entry.md) | Update local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/delete_cname_entry.yml`](../docs/playbooks/delete_cname_entry.md) | Delete CNAME entries from Pi-hole DNS server |
| [`dns/delete_dns_entry.yml`](../docs/playbooks/delete_dns_entry.md) | Delete local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/deploy_nebulasync.yml`](../docs/playbooks/deploy_nebulasync.md) | Deploy nebula-sync on the primary DNS server |
| [`dns/deploy_pihole.yml`](../docs/playbooks/deploy_pihole.md) | Deploy Pi-hole DNS server https://docs.pi-hole.net/main/basic-install/#alternative-1-clone-our-repository-and-run |
| [`dns/deploy_unbound.yml`](../docs/playbooks/deploy_unbound.md) | Deploy Unbound DNS resolver Based on Pi-hole documentation: https://docs.pi-hole.net/guides/dns/unbound/ |
| [`dns/restart_dns.yml`](../docs/playbooks/restart_dns.md) | Restart the DNS service on the Pi-hole DNS server |
| [`dns/show_cname_records.yml`](../docs/playbooks/show_cname_records.md) | Show CNAME records from Pi-hole DNS server |
| [`dns/show_config.yml`](../docs/playbooks/show_config.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/show_hosts.yml`](../docs/playbooks/show_hosts.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/update_pihole_dns.yml`](../docs/playbooks/update_pihole_dns.md) | Update DNS settings on the Pi-hole DNS server |
| [`docker/deploy_docker.yml`](../docs/playbooks/deploy_docker.md) | Deploy Docker on Docker hosts |
| [`geyser/deploy_geyser.yml`](../docs/playbooks/deploy_geyser.md) | Deploy Geyser Minecraft server proxy |
| [`grafana/backup_db.yml`](../docs/playbooks/backup_db.md) | Backup Grafana database to NFS share |
| [`grafana/create_db.yml`](../docs/playbooks/create_db.md) | Create PostgreSQL database for Grafana on the database server |
| [`grafana/deploy_grafana.yml`](../docs/playbooks/deploy_grafana.md) | Deploy Grafana monitoring tool on Grafana hosts |
| [`graphite/deploy_graphite.yml`](../docs/playbooks/deploy_graphite.md) | Install and configure Graphite monitoring tool on all hosts |
| [`graphite/restart_carbon_cache.yml`](../docs/playbooks/restart_carbon_cache.md) | Restart the carbon-cache service on Graphite hosts |
| [`graphite/start_carbon_cache.yml`](../docs/playbooks/start_carbon_cache.md) | Start the carbon-cache service on Graphite hosts |
| [`graphite/stop_carbon_cache.yml`](../docs/playbooks/stop_carbon_cache.md) | Stop the carbon-cache service on Graphite hosts |
| [`home-assistant/deploy_home-assistant.yml`](../docs/playbooks/deploy_home-assistant.md) | Deploy Home Assistant on a target host |
| [`java/deploy_java.yml`](../docs/playbooks/deploy_java.md) | Deploy Java runtime environment on Java hosts |
| [`jenkins/deploy_jenkins.yml`](../docs/playbooks/deploy_jenkins.md) | Deploy Jenkins automation server on Jenkins hosts |
| [`linux/check_connection.yml`](../docs/playbooks/check_connection.md) | Check connectivity and gather facts from Linux hosts |
| [`linux/check_cpu_usage.yml`](../docs/playbooks/check_cpu_usage.md) | Check CPU usage and zombie processes on Linux hosts |
| [`linux/check_diskspace.yml`](../docs/playbooks/check_diskspace.md) | Check disk space on Linux hosts |
| [`linux/check_failed_services.yml`](../docs/playbooks/check_failed_services.md) | Check for failed services on Linux hosts |
| [`linux/check_for_updates.yml`](../docs/playbooks/check_for_updates.md) | Check for available updates on Linux hosts |
| [`linux/check_logins.yml`](../docs/playbooks/check_logins.md) | Check for user logins and failed login attempts on Linux hosts |
| [`linux/check_mem_usage.yml`](../docs/playbooks/check_mem_usage.md) | Check memory usage on Linux hosts |
| [`linux/check_open_ports.yml`](../docs/playbooks/check_open_ports.md) | Check open ports on Linux hosts |
| [`linux/check_reboots.yml`](../docs/playbooks/check_reboots.md) | Check for recent reboots on Linux hosts |
| [`linux/check_syslog.yml`](../docs/playbooks/check_syslog.md) | Check system log entries on Linux hosts |
| [`linux/deploy_autofs.yml`](../docs/playbooks/deploy_autofs.md) | Deploys and configures autofs on designated servers. |
| [`linux/deploy_fstab.yml`](../docs/playbooks/deploy_fstab.md) | Manages fstab on designated servers. |
| [`linux/deploy_updates.yml`](../docs/playbooks/deploy_updates.md) | Deploy updates on Linux hosts |
| [`linux/remove_autofs.yml`](../docs/playbooks/remove_autofs.md) | Removes autofs from designated servers. |
| [`minecraft/check_bedrock_version.yml`](../docs/playbooks/check_bedrock_version.md) | Check latest Bedrock version on Bedrock hosts |
| [`minecraft/deploy_bedrock.yml`](../docs/playbooks/deploy_bedrock.md) | Deploy Minecraft Bedrock server |
| [`minecraft/deploy_minecraft.yml`](../docs/playbooks/deploy_minecraft.md) | Deploy Minecraft Java server |
| [`mongodb/deploy_mongodb.yml`](../docs/playbooks/deploy_mongodb.md) | Deploy MongoDB on MongoDB hosts |
| [`nginx/deploy_nginx.yml`](../docs/playbooks/deploy_nginx.md) | Deploy nginx on nginx hosts |
| [`oauth2_proxy/deploy_oauth2_proxy.yml`](../docs/playbooks/deploy_oauth2_proxy.md) | Deploy OAuth2 Proxy with Entra ID as the identity provider |
| [`ombi/backup_db.yml`](../docs/playbooks/backup_db.md) | Backup Ombi database to NFS share |
| [`ombi/create_db.yml`](../docs/playbooks/create_db.md) | Create Ombi PostgreSQL database on pgdb hosts |
| [`ombi/deploy_ombi.yml`](../docs/playbooks/deploy_ombi.md) | Deploy Ombi application on Ombi hosts |
| [`plex/backup_plex.yml`](../docs/playbooks/backup_plex.md) | Backup Plex Media Server configuration on plex hosts |
| [`plex/deploy_plex.yml`](../docs/playbooks/deploy_plex.md) | Install and configure Plex Media Server on plex hosts |
| [`postgresql/deploy_postgresql.yml`](../docs/playbooks/deploy_postgresql.md) | Install and configure PostgreSQL on pgdb hosts |
| [`prometheus/backup_db.yml`](../docs/playbooks/backup_db.md) | Backup Prometheus database to NFS share |
| [`prometheus/deploy_node_exporter.yml`](../docs/playbooks/deploy_node_exporter.md) | Deploy Node Exporter on Prometheus hosts |
| [`prometheus/deploy_prometheus.yml`](../docs/playbooks/deploy_prometheus.md) | Deploy Prometheus monitoring system |
| [`proxmox/deploy_ceph.yml`](../docs/playbooks/deploy_ceph.md) | Install Ceph storage cluster on Proxmox nodes |
| [`proxmox/deploy_pbs.yml`](../docs/playbooks/deploy_pbs.md) | Install Proxmox Backup Server on pbs hosts |
| [`pxe/configure_pxe.yml`](../docs/playbooks/configure_pxe.md) | Configure PXE on pxe_client hosts |
| [`pxe/deploy_pxe.yml`](../docs/playbooks/deploy_pxe.md) | Deploy PXE server on pxe hosts |
| [`python/bootstrap_python3.yml`](../docs/playbooks/bootstrap_python3.md) | Installs Python3 on hosts that do not yet have Python. This is typically used when provisioning new hosts that lack Python3, which is required for Ansible to function. This playbook also sets up a Python virtual environment |
| [`python/compile_python3.yml`](../docs/playbooks/compile_python3.md) | Compile and install Python3 on pvenodes hosts. This is necessary for Proxmox VE nodes where a newer Python version is required but not available via standard package repositories. |
| [`python/deploy_python3.yml`](../docs/playbooks/deploy_python3.md) | Deploy Python3 on python hosts. |
| [`python/deploy_python3_venv.yml`](../docs/playbooks/deploy_python3_venv.md) | Deploy Python3 virtual environment on python hosts. |
| [`redis/deploy_redis.yml`](../docs/playbooks/deploy_redis.md) | Deploy Redis server on redis hosts. |
| [`redmine/backup_db.yml`](../docs/playbooks/backup_db.md) | Backup Redmine database to NFS share. |
| [`redmine/create_db.yml`](../docs/playbooks/create_db.md) | Create PostgreSQL database for Redmine application. |
| [`redmine/deploy_redmine.yml`](../docs/playbooks/deploy_redmine.md) | Deploy Redmine application on redmine hosts. |
| [`redmine/mirror_wiki.yml`](../docs/playbooks/mirror_wiki.md) | Mirror Redmine wiki to GitHub |
| [`rproxy/config_rproxy.yml`](../docs/playbooks/config_rproxy.md) | Configures Reverse Proxy for specified sites. rproxy_setup_sites variable should be defined in the inventory or host_vars. |
| [`rproxy/deploy_rproxy.yml`](../docs/playbooks/deploy_rproxy.md) | Sets up Reverse Proxy on rproxy hosts. |
| [`ruby/deploy_ruby.yml`](../docs/playbooks/deploy_ruby.md) | Installs Ruby on ruby hosts. |
| [`semaphoreui/backup_db.yml`](../docs/playbooks/backup_db.md) | Backup Semaphore UI database to NFS share. |
| [`semaphoreui/check_semaphore_version.yml`](../docs/playbooks/check_semaphore_version.md) | Check the latest version of SemaphoreUI available. |
| [`semaphoreui/create_db.yml`](../docs/playbooks/create_db.md) | Create PostgreSQL database for Semaphore UI application. |
| [`semaphoreui/deploy_semaphoreui.yml`](../docs/playbooks/deploy_semaphoreui.md) | Installs Semaphore UI application on semaphore hosts. |
| [`semaphoreui/setup_semaphoreui.yml`](../docs/playbooks/setup_semaphoreui.md) | Sets up Semaphore UI application on semaphore hosts. It configures the Semaphore using the values in the semaphoreui_setup_projects variable. This playbook assumes that Semaphore UI has been installed. |
| [`services/backup_lidarr_db.yml`](../docs/playbooks/backup_lidarr_db.md) | Backup Lidarr database to NFS share. |
| [`services/backup_radarr_db.yml`](../docs/playbooks/backup_radarr_db.md) | Backup Radarr database to NFS share. |
| [`services/backup_sonarr_db.yml`](../docs/playbooks/backup_sonarr_db.md) | Backup Sonarr database to NFS share. |
| [`services/configure_lazylibrarian.yml`](../docs/playbooks/configure_lazylibrarian.md) | Configure Lazy Librarian application. |
| [`services/create_lidarr_db.yml`](../docs/playbooks/create_lidarr_db.md) | Create Lidarr PostgreSQL database. |
| [`services/create_radarr_db.yml`](../docs/playbooks/create_radarr_db.md) | Create Radarr PostgreSQL database. |
| [`services/create_sonarr_db.yml`](../docs/playbooks/create_sonarr_db.md) | Create Sonarr PostgreSQL database. |
| [`services/deploy_calibre.yml`](../docs/playbooks/deploy_calibre.md) | Installs Calibre application. |
| [`services/deploy_calibreweb.yml`](../docs/playbooks/deploy_calibreweb.md) | Installs Calibreweb application. |
| [`services/deploy_lazylibrarian.yml`](../docs/playbooks/deploy_lazylibrarian.md) | Installs Lazy Librarian application. |
| [`services/deploy_lidarr.yml`](../docs/playbooks/deploy_lidarr.md) | Installs Lidarr application. |
| [`services/deploy_radarr.yml`](../docs/playbooks/deploy_radarr.md) | Installs Radarr application. |
| [`services/deploy_sabnzbd.yml`](../docs/playbooks/deploy_sabnzbd.md) | Installs Sabnzbd application. |
| [`services/deploy_sonarr.yml`](../docs/playbooks/deploy_sonarr.md) | Installs Sonarr application. |
| [`services/start_all.yml`](../docs/playbooks/start_all.md) | Starts all media services. |
| [`services/start_lidarr.yml`](../docs/playbooks/start_lidarr.md) | Starts Lidarr service. |
| [`services/start_radarr.yml`](../docs/playbooks/start_radarr.md) | Starts Radarr service. |
| [`services/start_sabnzbd.yml`](../docs/playbooks/start_sabnzbd.md) | Starts Sabnzbd service. |
| [`services/start_sonarr.yml`](../docs/playbooks/start_sonarr.md) | Start Sonarr service |
| [`services/stop_all.yml`](../docs/playbooks/stop_all.md) | Stops all media services |
| [`services/stop_lidarr.yml`](../docs/playbooks/stop_lidarr.md) | Stops Lidarr service |
| [`services/stop_radarr.yml`](../docs/playbooks/stop_radarr.md) | Stops Lidarr service |
| [`services/stop_sabnzbd.yml`](../docs/playbooks/stop_sabnzbd.md) | Stops Sabnzbd service |
| [`services/stop_sonarr.yml`](../docs/playbooks/stop_sonarr.md) | Stops Sonarr service |
| [`synology/prep_ansible.yml`](../docs/playbooks/prep_ansible.md) | Prepares Synology NAS for Ansible management by configuring DNS entries, reverse proxy, and Python environment. |
| [`tautulli/backup_db.yml`](../docs/playbooks/backup_db.md) | Backs up Tautulli database and configuration files to a specified NFS share. |
| [`tautulli/deploy_tautulli.yml`](../docs/playbooks/deploy_tautulli.md) | Deploys Tautulli media tracking service with necessary configurations and NFS mounts. |
| [`template/create_template.yml`](../docs/playbooks/create_template.md) | Creates a VM template using cloud-init on the specified Proxmox node. |
| [`terraform/deploy_terraform.yml`](../docs/playbooks/deploy_terraform.md) | Installs Terraform |
| [`tplink/deploy_omada_controller.yml`](../docs/playbooks/deploy_omada_controller.md) | Installs and configures Tp-Link Omada Controller |
| [`ubuntu/check_ubuntu_install.yml`](../docs/playbooks/check_ubuntu_install.md) | Checks if Ubuntu is installed on the target machine |
| [`vault/config.yml`](../docs/playbooks/config.md) | Configures HashiCorp Vault on designated vault servers. |
| [`vault/create_ca.yml`](../docs/playbooks/create_ca.md) | Creates a Certificate Authority and Vault server certificate for HashiCorp Vault. |
| [`vault/create_vault_cert.yml`](../docs/playbooks/create_vault_cert.md) | Creates a Vault server certificate using an existing Certificate Authority for HashiCorp Vault. |
| [`vault/deploy_cacert_to_clients.yml`](../docs/playbooks/deploy_cacert_to_clients.md) | Deploys the Vault CA public certificate to all Vault client machines. |
| [`vault/deploy_vault.yml`](../docs/playbooks/deploy_vault.md) | Deploys HashiCorp Vault including installation, CA creation, server certificate creation, configuration, and CA certificate deployment to clients. |
| [`vault/install.yml`](../docs/playbooks/install.md) | Installs HashiCorp Vault on designated vault servers. |
| [`vault/remove_vault.yml`](../docs/playbooks/remove_vault.md) | Removes HashiCorp Vault from designated vault servers. |
| [`vms/add_disk.yml`](../docs/playbooks/add_disk.md) | Adds additional disks to virtual machines. |
| [`vms/add_users.yml`](../docs/playbooks/add_users.md) | Adds users to virtual machines and bare metal servers. |
| [`vms/convert_to_template.yml`](../docs/playbooks/convert_to_template.md) | Converts virtual machines to templates. |
| [`vms/create_cloud_init_iso.yml`](../docs/playbooks/create_cloud_init_iso.md) | Creates a cloud-init ISO for virtual machines to enable autoinstallation. |
| [`vms/create_vm.yml`](../docs/playbooks/create_vm.md) | Creates virtual machines and manages their DNS entries. |
| [`vms/create_vm_snapshot.yml`](../docs/playbooks/create_vm_snapshot.md) | Creates snapshots of virtual machines. |
| [`vms/deploy_sshpass.yml`](../docs/playbooks/deploy_sshpass.md) | Deploys sshpass utility on virtual machines. |
| [`vms/force_reboot_vm.yml`](../docs/playbooks/force_reboot_vm.md) | Forces a reboot of virtual machines by stopping and starting them. |
| [`vms/install_vm_packages.yml`](../docs/playbooks/install_vm_packages.md) | Installs required packages on virtual machines. |
| [`vms/list_vm_snapshot.yml`](../docs/playbooks/list_vm_snapshot.md) | Lists snapshots of virtual machines. |
| [`vms/migrate_vm.yml`](../docs/playbooks/migrate_vm.md) | Migrates virtual machines to different hosts or storage. |
| [`vms/prep_disk.yml`](../docs/playbooks/prep_disk.md) | Prepares and formats local disks on virtual machines and bare metal servers. |
| [`vms/provision_vm.yml`](../docs/playbooks/provision_vm.md) | Provisions virtual machines using either Terraform or Ansible, managing DNS entries accordingly. |
| [`vms/reboot_vm.yml`](../docs/playbooks/reboot_vm.md) | Reboots virtual machines gracefully. |
| [`vms/remove_vm.yml`](../docs/playbooks/remove_vm.md) | Removes virtual machines using either Terraform or Ansible, with confirmation and DNS cleanup. |
| [`vms/remove_vm_snapshot.yml`](../docs/playbooks/remove_vm_snapshot.md) | Removes snapshots from virtual machines. |
| [`vms/revert_vm_snapshot.yml`](../docs/playbooks/revert_vm_snapshot.md) | Reverts virtual machines to a specified snapshot and starts them. |
| [`vms/set_dns_servers.yml`](../docs/playbooks/set_dns_servers.md) | Sets DNS servers on virtual machines and bare metal servers. |
| [`vms/show_vm_id.yml`](../docs/playbooks/show_vm_id.md) | Displays the VMID of virtual machines. |
| [`vms/show_vm_node.yml`](../docs/playbooks/show_vm_node.md) | Displays the Proxmox node hosting the specified virtual machines. |
| [`vms/shutdown_vm.yml`](../docs/playbooks/shutdown_vm.md) | Shuts down virtual machines gracefully. |
| [`vms/start_vm.yml`](../docs/playbooks/start_vm.md) | Starts a virtual machine. |
| [`vms/stop_vm.yml`](../docs/playbooks/stop_vm.md) | Stops a virtual machine. |
| [`vms/update_known_hosts.yml`](../docs/playbooks/update_known_hosts.md) | Updates the known_hosts file with the SSH fingerprints of all virtual machines. |
| [`vms/upgrade_vm_os.yml`](../docs/playbooks/upgrade_vm_os.md) | Upgrades the operating system of virtual machines. |
| [`wikipedia/deploy_wikipedia.yml`](../docs/playbooks/deploy_wikipedia.md) | Deploys a Wikipedia instance using various setup roles. |