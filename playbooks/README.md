# 📚 Playbook Index

## 📂 Playbooks in root `playbooks/`

| Playbook | Purpose |
|----------|---------|
| [`deploy_code_server.yml`](deploy_code_server.md) | Deploy and configure code-server on target hosts |
| [`deploy_vscode_server.yml`](deploy_vscode_server.md) | Deploy and configure VSCode Server on target hosts |
| [`provision_vm.yml`](provision_vm.md) | Provision a new VM and prepare it as an Ansible node |

## 📂 Playbooks in subfolders

| Playbook Path | Purpose |
|---------------|---------|
| [`ad/join_domain.yml`](ad/join_domain.md) | Join hosts to an Active Directory domain |
| [`ad/leave_domain.yml`](ad/leave_domain.md) | Remove hosts from an Active Directory domain |
| [`ansible/deploy_ansible.yml`](ansible/deploy_ansible.md) | Deploy and configure Ansible on the control node |
| [`ansible/install_python3_modules.yml`](ansible/install_python3_modules.md) | Install required Python 3 modules for Ansible operation |
| [`ansible/prep_ansible_node.yml`](ansible/prep_ansible_node.md) | Prepare nodes to be managed by Ansible |
| [`ansible/remove_python3_modules.yml`](ansible/remove_python3_modules.md) | Remove Python 3 modules no longer needed for Ansible operation |
| [`aws/deploy_aws_cli.yml`](aws/deploy_aws_cli.md) | Deploy AWS CLI on target hosts |
| [`azure/deploy_azure_cli.yml`](azure/deploy_azure_cli.md) | Deploy Azure CLI on target hosts |
| [`azure/deploy_azure_ps.yml`](azure/deploy_azure_ps.md) | Deploy Azure Powershell on the Ansible control node |
| [`azure/entra_id_for_oauth2.yml`](azure/entra_id_for_oauth2.md) | Configure Entra ID applications for OAuth2 authentication |
| [`baremetal/reboot.yml`](baremetal/reboot.md) | Reboot baremetal machines using the vms role's reboot tasks |
| [`baremetal/shutdown.yml`](baremetal/shutdown.md) | Unconditionally shut down baremetal machine with all defaults |
| [`certbot/deploy_certbot.yml`](certbot/deploy_certbot.md) | Deploy Certbot on target hosts |
| [`certs/distribute_pve_certs.yml`](certs/distribute_pve_certs.md) | Distribute web certificates from cert staging host to Proxmox nodes |
| [`certs/generate_certs.yml`](certs/generate_certs.md) | Generate Let’s Encrypt certbot certificates on the cert staging host |
| [`certs/stage_certs.yml`](certs/stage_certs.md) | Stage certificates on the cert staging host in preparation for use by reverse proxy and other services |
| [`dns/add_cname_entry.yml`](dns/add_cname_entry.md) | Add CNAME entries to Pi-hole DNS server |
| [`dns/add_dns_entry.yml`](dns/add_dns_entry.md) | Update local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/delete_cname_entry.yml`](dns/delete_cname_entry.md) | Delete CNAME entries from Pi-hole DNS server |
| [`dns/delete_dns_entry.yml`](dns/delete_dns_entry.md) | Delete local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/deploy_nebulasync.yml`](dns/deploy_nebulasync.md) | Deploy nebula-sync on the primary DNS server |
| [`dns/deploy_pihole.yml`](dns/deploy_pihole.md) | Deploy Pi-hole DNS server https://docs.pi-hole.net/main/basic-install/#alternative-1-clone-our-repository-and-run |
| [`dns/restart_dns.yml`](dns/restart_dns.md) | Restart the DNS service on the Pi-hole DNS server |
| [`dns/show_cname_records.yml`](dns/show_cname_records.md) | Show CNAME records from Pi-hole DNS server |
| [`dns/show_config.yml`](dns/show_config.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/show_hosts.yml`](dns/show_hosts.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/update_pihole_dns.yml`](dns/update_pihole_dns.md) | Update DNS settings on the Pi-hole DNS server |
| [`docker/deploy_docker.yml`](docker/deploy_docker.md) | Deploy Docker on Docker hosts |
| [`geyser/deploy_geyser.yml`](geyser/deploy_geyser.md) | Deploy Geyser Minecraft server proxy |
| [`grafana/backup_db.yml`](grafana/backup_db.md) | Backup Grafana database to NFS share |
| [`grafana/create_db.yml`](grafana/create_db.md) | Create PostgreSQL database for Grafana on the database server |
| [`grafana/deploy_grafana.yml`](grafana/deploy_grafana.md) | Deploy Grafana monitoring tool on Grafana hosts |
| [`graphite/deploy_graphite.yml`](graphite/deploy_graphite.md) | Install and configure Graphite monitoring tool on all hosts |
| [`graphite/restart_carbon_cache.yml`](graphite/restart_carbon_cache.md) | Restart the carbon-cache service on Graphite hosts |
| [`graphite/start_carbon_cache.yml`](graphite/start_carbon_cache.md) | Start the carbon-cache service on Graphite hosts |
| [`graphite/stop_carbon_cache.yml`](graphite/stop_carbon_cache.md) | Stop the carbon-cache service on Graphite hosts |
| [`java/deploy_java.yml`](java/deploy_java.md) | Deploy Java runtime environment on Java hosts |
| [`jenkins/deploy_jenkins.yml`](jenkins/deploy_jenkins.md) | Deploy Jenkins automation server on Jenkins hosts |
| [`linux/check_connection.yml`](linux/check_connection.md) | Check connectivity and gather facts from Linux hosts |
| [`linux/check_cpu_usage.yml`](linux/check_cpu_usage.md) | Check CPU usage and zombie processes on Linux hosts |
| [`linux/check_diskspace.yml`](linux/check_diskspace.md) | Check disk space on Linux hosts |
| [`linux/check_failed_services.yml`](linux/check_failed_services.md) | Check for failed services on Linux hosts |
| [`linux/check_for_updates.yml`](linux/check_for_updates.md) | Check for available updates on Linux hosts |
| [`linux/check_logins.yml`](linux/check_logins.md) | Check for user logins and failed login attempts on Linux hosts |
| [`linux/check_mem_usage.yml`](linux/check_mem_usage.md) | Check memory usage on Linux hosts |
| [`linux/check_open_ports.yml`](linux/check_open_ports.md) | Check open ports on Linux hosts |
| [`linux/check_reboots.yml`](linux/check_reboots.md) | Check for recent reboots on Linux hosts |
| [`linux/check_syslog.yml`](linux/check_syslog.md) | Check system log entries on Linux hosts |
| [`linux/deploy_updates.yml`](linux/deploy_updates.md) | Deploy updates on Linux hosts |
| [`minecraft/check_bedrock_version.yml`](minecraft/check_bedrock_version.md) | Check latest Bedrock version on Bedrock hosts |
| [`minecraft/deploy_bedrock.yml`](minecraft/deploy_bedrock.md) | Deploy Minecraft Bedrock server |
| [`minecraft/deploy_minecraft.yml`](minecraft/deploy_minecraft.md) | Deploy Minecraft Java server |
| [`mongodb/deploy_mongodb.yml`](mongodb/deploy_mongodb.md) | Deploy MongoDB on MongoDB hosts |
| [`nginx/deploy_nginx.yml`](nginx/deploy_nginx.md) | Deploy nginx on nginx hosts |
| [`oauth2_proxy/deploy_oauth2_proxy.yml`](oauth2_proxy/deploy_oauth2_proxy.md) | Deploy OAuth2 Proxy with Entra ID as the identity provider |
| [`ombi/backup_db.yml`](ombi/backup_db.md) | Backup Ombi database to NFS share |
| [`ombi/create_db.yml`](ombi/create_db.md) | Create Ombi PostgreSQL database on pgdb hosts |
| [`ombi/deploy_ombi.yml`](ombi/deploy_ombi.md) | Deploy Ombi application on Ombi hosts |
| [`plex/backup_plex.yml`](plex/backup_plex.md) | Backup Plex Media Server configuration on plex hosts |
| [`plex/deploy_plex.yml`](plex/deploy_plex.md) | Install and configure Plex Media Server on plex hosts |
| [`postgresql/deploy_postgresql.yml`](postgresql/deploy_postgresql.md) | Install and configure PostgreSQL on pgdb hosts |
| [`prometheus/backup_db.yml`](prometheus/backup_db.md) | Backup Prometheus database to NFS share |
| [`prometheus/deploy_node_exporter.yml`](prometheus/deploy_node_exporter.md) | Deploy Node Exporter on Prometheus hosts |
| [`prometheus/deploy_prometheus.yml`](prometheus/deploy_prometheus.md) | Deploy Prometheus monitoring system |
| [`proxmox/deploy_ceph.yml`](proxmox/deploy_ceph.md) | Install Ceph storage cluster on Proxmox nodes |
| [`proxmox/deploy_pbs.yml`](proxmox/deploy_pbs.md) | Install Proxmox Backup Server on pbs hosts |
| [`pxe/configure_pxe.yml`](pxe/configure_pxe.md) | Configure PXE on pxe_client hosts |
| [`pxe/deploy_pxe.yml`](pxe/deploy_pxe.md) | Deploy PXE server on pxe hosts |
| [`python/compile_python3.yml`](python/compile_python3.md) | Compile and install Python3 on pvenodes hosts. This is necessary for Proxmox VE nodes where a newer Python version is required but not available via standard package repositories. |
| [`python/deploy_python3.yml`](python/deploy_python3.md) | Deploy Python3 on python hosts. |
| [`python/deploy_python3_venv.yml`](python/deploy_python3_venv.md) | Deploy Python3 virtual environment on python hosts. |
| [`redis/deploy_redis.yml`](redis/deploy_redis.md) | Deploy Redis server on redis hosts. |
| [`redmine/backup_db.yml`](redmine/backup_db.md) | Backup Redmine database to NFS share. |
| [`redmine/create_db.yml`](redmine/create_db.md) | Create PostgreSQL database for Redmine application. |
| [`redmine/deploy_redmine.yml`](redmine/deploy_redmine.md) | Deploy Redmine application on redmine hosts. |
| [`rproxy/config_rproxy.yml`](rproxy/config_rproxy.md) | Configures Reverse Proxy for specified sites. rproxy_setup_sites variable should be defined in the inventory or host_vars. |
| [`rproxy/deploy_rproxy.yml`](rproxy/deploy_rproxy.md) | Sets up Reverse Proxy on rproxy hosts. |
| [`ruby/deploy_ruby.yml`](ruby/deploy_ruby.md) | Installs Ruby on ruby hosts. |
| [`semaphoreui/backup_db.yml`](semaphoreui/backup_db.md) | Backup Semaphore UI database to NFS share. |
| [`semaphoreui/check_semaphore_version.yml`](semaphoreui/check_semaphore_version.md) | Check the latest version of SemaphoreUI available. |
| [`semaphoreui/create_db.yml`](semaphoreui/create_db.md) | Create PostgreSQL database for Semaphore UI application. |
| [`semaphoreui/deploy_semaphoreui.yml`](semaphoreui/deploy_semaphoreui.md) | Installs Semaphore UI application on semaphore hosts. |
| [`semaphoreui/setup_semaphoreui.yml`](semaphoreui/setup_semaphoreui.md) | Sets up Semaphore UI application on semaphore hosts. It configures the Semaphore using the values in the semaphoreui_setup_projects variable. This playbook assumes that Semaphore UI has been installed. |
| [`services/backup_lidarr_db.yml`](services/backup_lidarr_db.md) | Backup Lidarr database to NFS share. |
| [`services/backup_radarr_db.yml`](services/backup_radarr_db.md) | Backup Radarr database to NFS share. |
| [`services/backup_sonarr_db.yml`](services/backup_sonarr_db.md) | Backup Sonarr database to NFS share. |
| [`services/configure_lazylibrarian.yml`](services/configure_lazylibrarian.md) | Configure Lazy Librarian application. |
| [`services/create_lidarr_db.yml`](services/create_lidarr_db.md) | Create Lidarr PostgreSQL database. |
| [`services/create_radarr_db.yml`](services/create_radarr_db.md) | Create Radarr PostgreSQL database. |
| [`services/create_sonarr_db.yml`](services/create_sonarr_db.md) | Create Sonarr PostgreSQL database. |
| [`services/deploy_calibre.yml`](services/deploy_calibre.md) | Installs Calibre application. |
| [`services/deploy_calibreweb.yml`](services/deploy_calibreweb.md) | Installs Calibreweb application. |
| [`services/deploy_lazylibrarian.yml`](services/deploy_lazylibrarian.md) | Installs Lazy Librarian application. |
| [`services/deploy_lidarr.yml`](services/deploy_lidarr.md) | Installs Lidarr application. |
| [`services/deploy_radarr.yml`](services/deploy_radarr.md) | Installs Radarr application. |
| [`services/deploy_sabnzbd.yml`](services/deploy_sabnzbd.md) | Installs Sabnzbd application. |
| [`services/deploy_sonarr.yml`](services/deploy_sonarr.md) | Installs Sonarr application. |
| [`services/start_all.yml`](services/start_all.md) | Starts all media services. |
| [`services/start_lidarr.yml`](services/start_lidarr.md) | Starts Lidarr service. |
| [`services/start_radarr.yml`](services/start_radarr.md) | Starts Radarr service. |
| [`services/start_sabnzbd.yml`](services/start_sabnzbd.md) | Starts Sabnzbd service. |
| [`services/start_sonarr.yml`](services/start_sonarr.md) | Start Sonarr service |
| [`services/stop_all.yml`](services/stop_all.md) | Stops all media services |
| [`services/stop_lidarr.yml`](services/stop_lidarr.md) | Stops Lidarr service |
| [`services/stop_radarr.yml`](services/stop_radarr.md) | Stops Lidarr service |
| [`services/stop_sabnzbd.yml`](services/stop_sabnzbd.md) | Stops Sabnzbd service |
| [`services/stop_sonarr.yml`](services/stop_sonarr.md) | Stops Sonarr service |
| [`synology/prep_ansible.yml`](synology/prep_ansible.md) | Prepares Synology NAS for Ansible management by configuring DNS entries, reverse proxy, and Python environment. |
| [`tautulli/backup_db.yml`](tautulli/backup_db.md) | Backs up Tautulli database and configuration files to a specified NFS share. |
| [`tautulli/deploy_tautulli.yml`](tautulli/deploy_tautulli.md) | Deploys Tautulli media tracking service with necessary configurations and NFS mounts. |
| [`template/create_template.yml`](template/create_template.md) | Creates a VM template using cloud-init on the specified Proxmox node. |
| [`terraform/deploy_terraform.yml`](terraform/deploy_terraform.md) | Installs Terraform |
| [`tplink/deploy_omada_controller.yml`](tplink/deploy_omada_controller.md) | Installs and configures Tp-Link Omada Controller |
| [`ubuntu/check_ubuntu_install.yml`](ubuntu/check_ubuntu_install.md) | Checks if Ubuntu is installed on the target machine |
| [`vault/config.yml`](vault/config.md) | Configures HashiCorp Vault on designated vault servers. |
| [`vault/create_ca.yml`](vault/create_ca.md) | Creates a Certificate Authority and Vault server certificate for HashiCorp Vault. |
| [`vault/create_vault_cert.yml`](vault/create_vault_cert.md) | Creates a Vault server certificate using an existing Certificate Authority for HashiCorp Vault. |
| [`vault/deploy_cacert_to_clients.yml`](vault/deploy_cacert_to_clients.md) | Deploys the Vault CA public certificate to all Vault client machines. |
| [`vault/deploy_vault.yml`](vault/deploy_vault.md) | Deploys HashiCorp Vault including installation, CA creation, server certificate creation, configuration, and CA certificate deployment to clients. |
| [`vault/install.yml`](vault/install.md) | Installs HashiCorp Vault on designated vault servers. |
| [`vault/remove_vault.yml`](vault/remove_vault.md) | Removes HashiCorp Vault from designated vault servers. |
| [`vms/add_disk.yml`](vms/add_disk.md) | Adds additional disks to virtual machines. |
| [`vms/add_users.yml`](vms/add_users.md) | Adds users to virtual machines and bare metal servers. |
| [`vms/convert_to_template.yml`](vms/convert_to_template.md) | Converts virtual machines to templates. |
| [`vms/create_cloud_init_iso.yml`](vms/create_cloud_init_iso.md) | Creates a cloud-init ISO for virtual machines to enable autoinstallation. |
| [`vms/create_vm.yml`](vms/create_vm.md) | Creates virtual machines and manages their DNS entries. |
| [`vms/create_vm_snapshot.yml`](vms/create_vm_snapshot.md) | Creates snapshots of virtual machines. |
| [`vms/deploy_autofs.yml`](vms/deploy_autofs.md) | Deploys and configures autofs on designated servers. |
| [`vms/deploy_sshpass.yml`](vms/deploy_sshpass.md) | Deploys sshpass utility on virtual machines. |
| [`vms/force_reboot_vm.yml`](vms/force_reboot_vm.md) | Forces a reboot of virtual machines by stopping and starting them. |
| [`vms/install_vm_packages.yml`](vms/install_vm_packages.md) | Installs required packages on virtual machines. |
| [`vms/list_vm_snapshot.yml`](vms/list_vm_snapshot.md) | Lists snapshots of virtual machines. |
| [`vms/migrate_vm.yml`](vms/migrate_vm.md) | Migrates virtual machines to different hosts or storage. |
| [`vms/prep_disk.yml`](vms/prep_disk.md) | Prepares and formats local disks on virtual machines and bare metal servers. |
| [`vms/provision_vm.yml`](vms/provision_vm.md) | Provisions virtual machines using either Terraform or Ansible, managing DNS entries accordingly. |
| [`vms/reboot_vm.yml`](vms/reboot_vm.md) | Reboots virtual machines gracefully. |
| [`vms/remove_vm.yml`](vms/remove_vm.md) | Removes virtual machines using either Terraform or Ansible, with confirmation and DNS cleanup. |
| [`vms/remove_vm_snapshot.yml`](vms/remove_vm_snapshot.md) | Removes snapshots from virtual machines. |
| [`vms/revert_vm_snapshot.yml`](vms/revert_vm_snapshot.md) | Reverts virtual machines to a specified snapshot and starts them. |
| [`vms/set_dns_servers.yml`](vms/set_dns_servers.md) | Sets DNS servers on virtual machines and bare metal servers. |
| [`vms/show_vm_id.yml`](vms/show_vm_id.md) | Displays the VMID of virtual machines. |
| [`vms/show_vm_node.yml`](vms/show_vm_node.md) | Displays the Proxmox node hosting the specified virtual machines. |
| [`vms/shutdown_vm.yml`](vms/shutdown_vm.md) | Shuts down virtual machines gracefully. |
| [`vms/start_vm.yml`](vms/start_vm.md) | Starts a virtual machine. |
| [`vms/stop_vm.yml`](vms/stop_vm.md) | Stops a virtual machine. |
| [`vms/update_known_hosts.yml`](vms/update_known_hosts.md) | Updates the known_hosts file with the SSH fingerprints of all virtual machines. |
| [`vms/upgrade_vm_os.yml`](vms/upgrade_vm_os.md) | Upgrades the operating system of virtual machines. |
| [`wikipedia/deploy_wikipedia.yml`](wikipedia/deploy_wikipedia.md) | Deploys a Wikipedia instance using various setup roles. |