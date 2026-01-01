# 📚 Playbook Index

## 📂 Playbooks in root `playbooks/`

| Playbook | Purpose |
|----------|---------|
| [`deploy_code_server.yml`](deploy_code_server.md) | Deploy and configure code-server on target hosts |
| [`deploy_vscode_server.yml`](deploy_vscode_server.md) | Deploy and configure VSCode Server on target hosts |
| [`disable_code_server.yml`](disable_code_server.md) | Stop and disable code-server on target hosts |
| [`enable_code_server.yml`](enable_code_server.md) | Start and enable code-server on target hosts |
| [`provision_vm.yml`](provision_vm.md) | Provision a new VM and prepare it as an Ansible node |

## 📂 Playbooks in subfolders

| Playbook Path | Purpose |
|---------------|---------|
| [`ad/join_domain.yml`](join_domain.md) | Join hosts to an Active Directory domain |
| [`ad/leave_domain.yml`](leave_domain.md) | Remove hosts from an Active Directory domain |
| [`ansible/deploy_ansible.yml`](deploy_ansible.md) | Deploy and configure Ansible on the control node |
| [`ansible/install_python3_modules.yml`](install_python3_modules.md) | Install required Python 3 modules for Ansible operation |
| [`ansible/prep_ansible_node.yml`](prep_ansible_node.md) | Prepare nodes to be managed by Ansible |
| [`ansible/remove_python3_modules.yml`](remove_python3_modules.md) | Remove Python 3 modules no longer needed for Ansible operation |
| [`aws/deploy_aws_cli.yml`](deploy_aws_cli.md) | Deploy AWS CLI on target hosts |
| [`azure/deploy_azure_cli.yml`](deploy_azure_cli.md) | Deploy Azure CLI on target hosts |
| [`azure/deploy_azure_ps.yml`](deploy_azure_ps.md) | Deploy Azure Powershell on the Ansible control node |
| [`azure/entra_id_for_oauth2.yml`](entra_id_for_oauth2.md) | Configure Entra ID applications for OAuth2 authentication |
| [`baremetal/reboot.yml`](reboot.md) | Reboot baremetal machines using the vms role's reboot tasks |
| [`baremetal/shutdown.yml`](shutdown.md) | Unconditionally shut down baremetal machine with all defaults |
| [`certbot/deploy_certbot.yml`](deploy_certbot.md) | Deploy Certbot on target hosts |
| [`certs/distribute_pve_certs.yml`](distribute_pve_certs.md) | Distribute web certificates from cert staging host to Proxmox nodes |
| [`certs/generate_all_certs.yml`](generate_all_certs.md) | Generate Let’s Encrypt certbot certificates for every domain |
| [`certs/generate_certs.yml`](generate_certs.md) | Generate Let’s Encrypt certbot certificates on the cert staging host |
| [`certs/stage_all_certs.yml`](stage_all_certs.md) | Stage all certificates on the cert staging host in preparation for use by reverse proxy and other services |
| [`certs/stage_certs.yml`](stage_certs.md) | Stage certificates on the cert staging host in preparation for use by reverse proxy and other services |
| [`dns/add_cname_entry.yml`](add_cname_entry.md) | Add CNAME entries to Pi-hole DNS server |
| [`dns/add_dns_entry.yml`](add_dns_entry.md) | Update local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/delete_cname_entry.yml`](delete_cname_entry.md) | Delete CNAME entries from Pi-hole DNS server |
| [`dns/delete_dns_entry.yml`](delete_dns_entry.md) | Delete local DNS entries in Pi-hole for VMs, Synology, and Proxmox nodes |
| [`dns/deploy_nebulasync.yml`](deploy_nebulasync.md) | Deploy nebula-sync on the primary DNS server |
| [`dns/deploy_pihole.yml`](deploy_pihole.md) | Deploy Pi-hole DNS server https://docs.pi-hole.net/main/basic-install/#alternative-1-clone-our-repository-and-run |
| [`dns/deploy_unbound.yml`](deploy_unbound.md) | Deploy Unbound DNS resolver Based on Pi-hole documentation: https://docs.pi-hole.net/guides/dns/unbound/ |
| [`dns/restart_dns.yml`](restart_dns.md) | Restart the DNS service on the Pi-hole DNS server |
| [`dns/show_cname_records.yml`](show_cname_records.md) | Show CNAME records from Pi-hole DNS server |
| [`dns/show_config.yml`](show_config.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/show_hosts.yml`](show_hosts.md) | Show the current configuration of the Pi-hole DNS server |
| [`dns/update_pihole_dns.yml`](update_pihole_dns.md) | Update DNS settings on the Pi-hole DNS server |
| [`docker/deploy_docker.yml`](deploy_docker.md) | Deploy Docker on Docker hosts |
| [`geyser/deploy_geyser.yml`](deploy_geyser.md) | Deploy Geyser Minecraft server proxy |
| [`grafana/backup_db.yml`](backup_db.md) | Backup Grafana database to NFS share |
| [`grafana/create_db.yml`](create_db.md) | Create PostgreSQL database for Grafana on the database server |
| [`grafana/deploy_grafana.yml`](deploy_grafana.md) | Deploy Grafana monitoring tool on Grafana hosts |
| [`graphite/deploy_graphite.yml`](deploy_graphite.md) | Install and configure Graphite monitoring tool on all hosts |
| [`graphite/restart_carbon_cache.yml`](restart_carbon_cache.md) | Restart the carbon-cache service on Graphite hosts |
| [`graphite/start_carbon_cache.yml`](start_carbon_cache.md) | Start the carbon-cache service on Graphite hosts |
| [`graphite/stop_carbon_cache.yml`](stop_carbon_cache.md) | Stop the carbon-cache service on Graphite hosts |
| [`java/deploy_java.yml`](deploy_java.md) | Deploy Java runtime environment on Java hosts |
| [`jenkins/deploy_jenkins.yml`](deploy_jenkins.md) | Deploy Jenkins automation server on Jenkins hosts |
| [`linux/check_connection.yml`](check_connection.md) | Check connectivity and gather facts from Linux hosts |
| [`linux/check_cpu_usage.yml`](check_cpu_usage.md) | Check CPU usage and zombie processes on Linux hosts |
| [`linux/check_diskspace.yml`](check_diskspace.md) | Check disk space on Linux hosts |
| [`linux/check_failed_services.yml`](check_failed_services.md) | Check for failed services on Linux hosts |
| [`linux/check_for_updates.yml`](check_for_updates.md) | Check for available updates on Linux hosts |
| [`linux/check_logins.yml`](check_logins.md) | Check for user logins and failed login attempts on Linux hosts |
| [`linux/check_mem_usage.yml`](check_mem_usage.md) | Check memory usage on Linux hosts |
| [`linux/check_open_ports.yml`](check_open_ports.md) | Check open ports on Linux hosts |
| [`linux/check_reboots.yml`](check_reboots.md) | Check for recent reboots on Linux hosts |
| [`linux/check_syslog.yml`](check_syslog.md) | Check system log entries on Linux hosts |
| [`linux/deploy_updates.yml`](deploy_updates.md) | Deploy updates on Linux hosts |
| [`minecraft/check_bedrock_version.yml`](check_bedrock_version.md) | Check latest Bedrock version on Bedrock hosts |
| [`minecraft/deploy_bedrock.yml`](deploy_bedrock.md) | Deploy Minecraft Bedrock server |
| [`minecraft/deploy_minecraft.yml`](deploy_minecraft.md) | Deploy Minecraft Java server |
| [`mongodb/deploy_mongodb.yml`](deploy_mongodb.md) | Deploy MongoDB on MongoDB hosts |
| [`nginx/deploy_nginx.yml`](deploy_nginx.md) | Deploy nginx on nginx hosts |
| [`oauth2_proxy/deploy_oauth2_proxy.yml`](deploy_oauth2_proxy.md) | Deploy OAuth2 Proxy with Entra ID as the identity provider |
| [`ombi/backup_db.yml`](backup_db.md) | Backup Ombi database to NFS share |
| [`ombi/create_db.yml`](create_db.md) | Create Ombi PostgreSQL database on pgdb hosts |
| [`ombi/deploy_ombi.yml`](deploy_ombi.md) | Deploy Ombi application on Ombi hosts |
| [`plex/backup_plex.yml`](backup_plex.md) | Backup Plex Media Server configuration on plex hosts |
| [`plex/deploy_plex.yml`](deploy_plex.md) | Install and configure Plex Media Server on plex hosts |
| [`postgresql/deploy_postgresql.yml`](deploy_postgresql.md) | Install and configure PostgreSQL on pgdb hosts |
| [`prometheus/backup_db.yml`](backup_db.md) | Backup Prometheus database to NFS share |
| [`prometheus/deploy_node_exporter.yml`](deploy_node_exporter.md) | Deploy Node Exporter on Prometheus hosts |
| [`prometheus/deploy_prometheus.yml`](deploy_prometheus.md) | Deploy Prometheus monitoring system |
| [`proxmox/deploy_ceph.yml`](deploy_ceph.md) | Install Ceph storage cluster on Proxmox nodes |
| [`proxmox/deploy_pbs.yml`](deploy_pbs.md) | Install Proxmox Backup Server on pbs hosts |
| [`pxe/configure_pxe.yml`](configure_pxe.md) | Configure PXE on pxe_client hosts |
| [`pxe/deploy_pxe.yml`](deploy_pxe.md) | Deploy PXE server on pxe hosts |
| [`python/bootstrap_python3.yml`](bootstrap_python3.md) | Installs Python3 on hosts that do not yet have Python. This is typically used when provisioning new hosts that lack Python3, which is required for Ansible to function. This playbook also sets up a Python virtual environment |
| [`python/compile_python3.yml`](compile_python3.md) | Compile and install Python3 on pvenodes hosts. This is necessary for Proxmox VE nodes where a newer Python version is required but not available via standard package repositories. |
| [`python/deploy_python3.yml`](deploy_python3.md) | Deploy Python3 on python hosts. |
| [`python/deploy_python3_venv.yml`](deploy_python3_venv.md) | Deploy Python3 virtual environment on python hosts. |
| [`redis/deploy_redis.yml`](deploy_redis.md) | Deploy Redis server on redis hosts. |
| [`redmine/backup_db.yml`](backup_db.md) | Backup Redmine database to NFS share. |
| [`redmine/create_db.yml`](create_db.md) | Create PostgreSQL database for Redmine application. |
| [`redmine/deploy_redmine.yml`](deploy_redmine.md) | Deploy Redmine application on redmine hosts. |
| [`redmine/mirror_wiki.yml`](mirror_wiki.md) | Mirror Redmine wiki to GitHub |
| [`rproxy/config_rproxy.yml`](config_rproxy.md) | Configures Reverse Proxy for specified sites. rproxy_setup_sites variable should be defined in the inventory or host_vars. |
| [`rproxy/deploy_rproxy.yml`](deploy_rproxy.md) | Sets up Reverse Proxy on rproxy hosts. |
| [`ruby/deploy_ruby.yml`](deploy_ruby.md) | Installs Ruby on ruby hosts. |
| [`semaphoreui/backup_db.yml`](backup_db.md) | Backup Semaphore UI database to NFS share. |
| [`semaphoreui/check_semaphore_version.yml`](check_semaphore_version.md) | Check the latest version of SemaphoreUI available. |
| [`semaphoreui/create_db.yml`](create_db.md) | Create PostgreSQL database for Semaphore UI application. |
| [`semaphoreui/deploy_semaphoreui.yml`](deploy_semaphoreui.md) | Installs Semaphore UI application on semaphore hosts. |
| [`semaphoreui/setup_semaphoreui.yml`](setup_semaphoreui.md) | Sets up Semaphore UI application on semaphore hosts. It configures the Semaphore using the values in the semaphoreui_setup_projects variable. This playbook assumes that Semaphore UI has been installed. |
| [`services/backup_lidarr_db.yml`](backup_lidarr_db.md) | Backup Lidarr database to NFS share. |
| [`services/backup_radarr_db.yml`](backup_radarr_db.md) | Backup Radarr database to NFS share. |
| [`services/backup_sonarr_db.yml`](backup_sonarr_db.md) | Backup Sonarr database to NFS share. |
| [`services/configure_lazylibrarian.yml`](configure_lazylibrarian.md) | Configure Lazy Librarian application. |
| [`services/create_lidarr_db.yml`](create_lidarr_db.md) | Create Lidarr PostgreSQL database. |
| [`services/create_radarr_db.yml`](create_radarr_db.md) | Create Radarr PostgreSQL database. |
| [`services/create_sonarr_db.yml`](create_sonarr_db.md) | Create Sonarr PostgreSQL database. |
| [`services/deploy_calibre.yml`](deploy_calibre.md) | Installs Calibre application. |
| [`services/deploy_calibreweb.yml`](deploy_calibreweb.md) | Installs Calibreweb application. |
| [`services/deploy_lazylibrarian.yml`](deploy_lazylibrarian.md) | Installs Lazy Librarian application. |
| [`services/deploy_lidarr.yml`](deploy_lidarr.md) | Installs Lidarr application. |
| [`services/deploy_radarr.yml`](deploy_radarr.md) | Installs Radarr application. |
| [`services/deploy_sabnzbd.yml`](deploy_sabnzbd.md) | Installs Sabnzbd application. |
| [`services/deploy_sonarr.yml`](deploy_sonarr.md) | Installs Sonarr application. |
| [`services/start_all.yml`](start_all.md) | Starts all media services. |
| [`services/start_lidarr.yml`](start_lidarr.md) | Starts Lidarr service. |
| [`services/start_radarr.yml`](start_radarr.md) | Starts Radarr service. |
| [`services/start_sabnzbd.yml`](start_sabnzbd.md) | Starts Sabnzbd service. |
| [`services/start_sonarr.yml`](start_sonarr.md) | Start Sonarr service |
| [`services/stop_all.yml`](stop_all.md) | Stops all media services |
| [`services/stop_lidarr.yml`](stop_lidarr.md) | Stops Lidarr service |
| [`services/stop_radarr.yml`](stop_radarr.md) | Stops Lidarr service |
| [`services/stop_sabnzbd.yml`](stop_sabnzbd.md) | Stops Sabnzbd service |
| [`services/stop_sonarr.yml`](stop_sonarr.md) | Stops Sonarr service |
| [`synology/prep_ansible.yml`](prep_ansible.md) | Prepares Synology NAS for Ansible management by configuring DNS entries, reverse proxy, and Python environment. |
| [`tautulli/backup_db.yml`](backup_db.md) | Backs up Tautulli database and configuration files to a specified NFS share. |
| [`tautulli/deploy_tautulli.yml`](deploy_tautulli.md) | Deploys Tautulli media tracking service with necessary configurations and NFS mounts. |
| [`template/create_template.yml`](create_template.md) | Creates a VM template using cloud-init on the specified Proxmox node. |
| [`terraform/deploy_terraform.yml`](deploy_terraform.md) | Installs Terraform |
| [`tplink/deploy_omada_controller.yml`](deploy_omada_controller.md) | Installs and configures Tp-Link Omada Controller |
| [`ubuntu/check_ubuntu_install.yml`](check_ubuntu_install.md) | Checks if Ubuntu is installed on the target machine |
| [`vault/config.yml`](config.md) | Configures HashiCorp Vault on designated vault servers. |
| [`vault/create_ca.yml`](create_ca.md) | Creates a Certificate Authority and Vault server certificate for HashiCorp Vault. |
| [`vault/create_vault_cert.yml`](create_vault_cert.md) | Creates a Vault server certificate using an existing Certificate Authority for HashiCorp Vault. |
| [`vault/deploy_cacert_to_clients.yml`](deploy_cacert_to_clients.md) | Deploys the Vault CA public certificate to all Vault client machines. |
| [`vault/deploy_vault.yml`](deploy_vault.md) | Deploys HashiCorp Vault including installation, CA creation, server certificate creation, configuration, and CA certificate deployment to clients. |
| [`vault/install.yml`](install.md) | Installs HashiCorp Vault on designated vault servers. |
| [`vault/remove_vault.yml`](remove_vault.md) | Removes HashiCorp Vault from designated vault servers. |
| [`vms/add_disk.yml`](add_disk.md) | Adds additional disks to virtual machines. |
| [`vms/add_users.yml`](add_users.md) | Adds users to virtual machines and bare metal servers. |
| [`vms/convert_to_template.yml`](convert_to_template.md) | Converts virtual machines to templates. |
| [`vms/create_cloud_init_iso.yml`](create_cloud_init_iso.md) | Creates a cloud-init ISO for virtual machines to enable autoinstallation. |
| [`vms/create_vm.yml`](create_vm.md) | Creates virtual machines and manages their DNS entries. |
| [`vms/create_vm_snapshot.yml`](create_vm_snapshot.md) | Creates snapshots of virtual machines. |
| [`vms/deploy_autofs.yml`](deploy_autofs.md) | Deploys and configures autofs on designated servers. |
| [`vms/deploy_sshpass.yml`](deploy_sshpass.md) | Deploys sshpass utility on virtual machines. |
| [`vms/force_reboot_vm.yml`](force_reboot_vm.md) | Forces a reboot of virtual machines by stopping and starting them. |
| [`vms/install_vm_packages.yml`](install_vm_packages.md) | Installs required packages on virtual machines. |
| [`vms/list_vm_snapshot.yml`](list_vm_snapshot.md) | Lists snapshots of virtual machines. |
| [`vms/migrate_vm.yml`](migrate_vm.md) | Migrates virtual machines to different hosts or storage. |
| [`vms/prep_disk.yml`](prep_disk.md) | Prepares and formats local disks on virtual machines and bare metal servers. |
| [`vms/provision_vm.yml`](provision_vm.md) | Provisions virtual machines using either Terraform or Ansible, managing DNS entries accordingly. |
| [`vms/reboot_vm.yml`](reboot_vm.md) | Reboots virtual machines gracefully. |
| [`vms/remove_vm.yml`](remove_vm.md) | Removes virtual machines using either Terraform or Ansible, with confirmation and DNS cleanup. |
| [`vms/remove_vm_snapshot.yml`](remove_vm_snapshot.md) | Removes snapshots from virtual machines. |
| [`vms/revert_vm_snapshot.yml`](revert_vm_snapshot.md) | Reverts virtual machines to a specified snapshot and starts them. |
| [`vms/set_dns_servers.yml`](set_dns_servers.md) | Sets DNS servers on virtual machines and bare metal servers. |
| [`vms/show_vm_id.yml`](show_vm_id.md) | Displays the VMID of virtual machines. |
| [`vms/show_vm_node.yml`](show_vm_node.md) | Displays the Proxmox node hosting the specified virtual machines. |
| [`vms/shutdown_vm.yml`](shutdown_vm.md) | Shuts down virtual machines gracefully. |
| [`vms/start_vm.yml`](start_vm.md) | Starts a virtual machine. |
| [`vms/stop_vm.yml`](stop_vm.md) | Stops a virtual machine. |
| [`vms/update_known_hosts.yml`](update_known_hosts.md) | Updates the known_hosts file with the SSH fingerprints of all virtual machines. |
| [`vms/upgrade_vm_os.yml`](upgrade_vm_os.md) | Upgrades the operating system of virtual machines. |
| [`wikipedia/deploy_wikipedia.yml`](deploy_wikipedia.md) | Deploys a Wikipedia instance using various setup roles. |