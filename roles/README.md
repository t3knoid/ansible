# 📚 Roles

| Role | Description | Documentation |
|------|-------------|----------------|
| `ad` | Installs the required packages in order for a node to join an active directory domain. Use the user ansible (e.g. -u ansible) when using this role | [View Documentation](../docs/roles/ad.md) |
| `ansible_node` | Configures a node to be used as an Ansible control node. | [View Documentation](../docs/roles/ansible_node.md) |
| `ansible_setup` | Provides tasks to install and configure Ansible on a control node. | [View Documentation](../docs/roles/ansible_setup.md) |
| `autofs` | Installs and configures autofs on Debian/Ubuntu. | [View Documentation](../docs/roles/autofs.md) |
| `aws_cli` | Installs and configures AWS CLI. | [View Documentation](../docs/roles/aws_cli.md) |
| `azure_cli_setup` | Installs Microsoft Azure CLI | [View Documentation](../docs/roles/azure_cli_setup.md) |
| `azure_ps_setup` | Installs Microsoft Azure PowerShell | [View Documentation](../docs/roles/azure_ps_setup.md) |
| `bedrock_setup` | Installs Minecraft Bedrock Server on Linux systems. | [View Documentation](../docs/roles/bedrock_setup.md) |
| `calibre_setup` | Installs and configures Calibre eBook management software. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre). | [View Documentation](../docs/roles/calibre_setup.md) |
| `calibreweb_setup` | Installs and configures Calibre-Web, a web-based eBook management application. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre-web). | [View Documentation](../docs/roles/calibreweb_setup.md) |
| `certbot_setup` | It deploys certbot following instructions documented in https://certbot.eff.org/instructions?ws=nginx&os=pip. Target hosts must be in a group named *[certbot]* in its inventory. Certbot is used to obtain SSL/TLS certificates from Let's Encrypt. | [View Documentation](../docs/roles/certbot_setup.md) |
| `certs` | Provides tasks to request and renew SSL/TLS certificates from Let's Encrypt. It also provides tasks to stage certificates for eventual use by the Nginx reverse proxy and other services. | [View Documentation](../docs/roles/certs.md) |
| `cloudinit` | Provides tasks to create a virtual machine with cloud-init support. | [View Documentation](../docs/roles/cloudinit.md) |
| `code_server` | Installs and configures code server. | [View Documentation](../docs/roles/code_server.md) |
| `disks` | Prepares an attached disk by formatting and mounting to a defined mountpoint. Removes mounts from fstab that is associated with a none existing device. | [View Documentation](../docs/roles/disks.md) |
| `docker_setup` | Installs Docker and Docker Compose on Debian/Ubuntu systems. | [View Documentation](../docs/roles/docker_setup.md) |
| `elasticsearch_setup` | Install and configure Elasticsearch on Debian/Ubuntu | [View Documentation](../docs/roles/elasticsearch_setup.md) |
| `entra_id_oauth2` | Configures entra_id settings for oAuth2-enabled sites. | [View Documentation](../docs/roles/entra_id_oauth2.md) |
| `fstab` | Manage fstab entries on Debian/Ubuntu. | [View Documentation](../docs/roles/fstab.md) |
| `geyser_setup` | Installs and configures GeyserMC on Debian/Ubuntu systems as documented at https://geysermc.org/wiki/geyser/setup/?host=self&platform=standalone | [View Documentation](../docs/roles/geyser_setup.md) |
| `global` | Provides global defaults common to all roles. It provides the IP definition of each host in the datacenter. Every host must be defined here with its corresponding IP address. Other global variables are also defined here. | [View Documentation](../docs/roles/global.md) |
| `grafana_setup` | Install and configure Grafana on Debian/Ubuntu | [View Documentation](../docs/roles/grafana_setup.md) |
| `graphite_setup` | Installs and configures Graphite on Debian/Ubuntu systems. | [View Documentation](../docs/roles/graphite_setup.md) |
| `home_assistant_setup` | Installs Home Assistant using its QCOW2 image on a Proxmox VE host. | [View Documentation](../docs/roles/home_assistant_setup.md) |
| `java_setup` | Installs and configures Java on Debian/Ubuntu systems. | [View Documentation](../docs/roles/java_setup.md) |
| `jenkins_setup` | Installs and configures Jenkins on Debian/Ubuntu systems. | [View Documentation](../docs/roles/jenkins_setup.md) |
| `lamp_setup` | Install and configure LAMP on Debian/Ubuntu. | [View Documentation](../docs/roles/lamp_setup.md) |
| `lazylibrarian_setup` | Installs and configures LazyLibrarian on Debian/Ubuntu systems. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lazylibrarian). | [View Documentation](../docs/roles/lazylibrarian_setup.md) |
| `lidarr_setup` | Installs and configures Lidarr on Debian/Ubuntu systems. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lidarr). | [View Documentation](../docs/roles/lidarr_setup.md) |
| `linux_updates` | The linux role contains tasks related to updating Linux updates. | [View Documentation](../docs/roles/linux_updates.md) |
| `mediawiki_setup` | Installs and configures MediaWiki on Ubuntu systems. | [View Documentation](../docs/roles/mediawiki_setup.md) |
| `minecraft_setup` | Installs Minecraft Server on Ubuntu and Debian systems (https://www.minecraft.net/en-us/download/server). | [View Documentation](../docs/roles/minecraft_setup.md) |
| `mongodb_setup` | Installs [MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/). | [View Documentation](../docs/roles/mongodb_setup.md) |
| `nebulasync_setup` | Installs nebula-sync as documented in its [GitHub page](https://github.com/lovelaze/nebula-sync?tab=readme-ov-file#installation). This role requires that pi-hole role is configured on the target host. The target host is assumed to be the first host listed in the "primary_dns" inventory group. | [View Documentation](../docs/roles/nebulasync_setup.md) |
| `nginx_setup` | Installs the nginx service. | [View Documentation](../docs/roles/nginx_setup.md) |
| `node_exporter_setup` | Installs Prometheus Node Exporter | [View Documentation](../docs/roles/node_exporter_setup.md) |
| `oauth2_proxy_setup` | Install and configure OAuth2 Proxy. | [View Documentation](../docs/roles/oauth2_proxy_setup.md) |
| `oc_setup` | Install and configure TP-Link Omada Controller on Ubuntu systems. | [View Documentation](../docs/roles/oc_setup.md) |
| `ombi_setup` | Ombi Setup installs and configures an Ombi Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/ombi) | [View Documentation](../docs/roles/ombi_setup.md) |
| `pbs` | Installs and configures Proxmox Backup Server on Ubuntu systems. | [View Documentation](../docs/roles/pbs.md) |
| `pihole` | Installs and configures Pi-hole on Ubuntu systems (https://pi-hole.net/). Provides tasks to manage Pi-hole settings and configurations. | [View Documentation](../docs/roles/pihole.md) |
| `playwright` | Installs playwright. | [View Documentation](../docs/roles/playwright.md) |
| `pve` | Contains tasks to manage the Proxmox Virtual Environment | [View Documentation](../docs/roles/pve.md) |
| `pxeserver_setup` | The pxeserver_setup role is used to install and configure a [PXE server](https://ubuntu.com/server/docs/how-to-netboot-the-server-installer-on-amd64). For this to work under TP-Link Omada router, enable the "Legal DHCP Servers" setting and set it to the PXE server IP address. | [View Documentation](../docs/roles/pxeserver_setup.md) |
| `python3` | Installs Python 3 from the Python Software Foundation (PSF) repository. There is also an alternate option is to compile Python 3 from source. | [View Documentation](../docs/roles/python3.md) |
| `radarr_setup` | Installs and configures a Radarr Docker container. It uses an image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/radarr). | [View Documentation](../docs/roles/radarr_setup.md) |
| `redis_setup` | Installs and configures Redis. | [View Documentation](../docs/roles/redis_setup.md) |
| `redmine_setup` | Redmine Setup installs and configures an [Redmine](https://www.redmine.org/). The installation instructions are taken directly from [Redmine's installation guide](https://www.redmine.org/projects/redmine/wiki/RedmineInstall) and adapting [redmineadvisor.com's instructions](https://www.redmineadvisor.com/articles/6_0/install/ubuntu24/) on installing Redmine in Ubuntu 24. | [View Documentation](../docs/roles/redmine_setup.md) |
| `rproxy_setup` | rproxy_setup configures reverse proxy with failover support using nginx. This role requires at least three hosts to be defined. One host is configure as the main frontend proxy, the other two acts as the primary and secondary proxy. | [View Documentation](../docs/roles/rproxy_setup.md) |
| `ruby_setup` | The ruby_setup role builds and install Ruby from it's [https://www.ruby-lang.org/en/downloads/](source code). | [View Documentation](../docs/roles/ruby_setup.md) |
| `sabnzbd_setup` | Installs and configures a Sabnzbd Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sabnzbd). | [View Documentation](../docs/roles/sabnzbd_setup.md) |
| `semaphoreui_setup` | Installs and configures [Semaphore UI](https://docs.semaphoreui.com/). | [View Documentation](../docs/roles/semaphoreui_setup.md) |
| `sonarr_setup` | Installs and configures a Sonarr Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sonarr). | [View Documentation](../docs/roles/sonarr_setup.md) |
| `sshpass` | Installs sshpass from apt repositories. | [View Documentation](../docs/roles/sshpass.md) |
| `synology` | Provides tasks to manage Synology NAS devices. | [View Documentation](../docs/roles/synology.md) |
| `tautulli_setup` | Installs and configures an Tautulli Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/tautulli). | [View Documentation](../docs/roles/tautulli_setup.md) |
| `terraform_setup` | Installs Terraform | [View Documentation](../docs/roles/terraform_setup.md) |
| `unbound` | Installs and configures Unbound DNS resolver with optional logging support. | [View Documentation](../docs/roles/unbound.md) |
| `users` | Provides tasks to manage system users in Ubuntu and Debian. | [View Documentation](../docs/roles/users.md) |
| `vault_setup` | Installs and configures Hashicorp Vault | [View Documentation](../docs/roles/vault_setup.md) |
| `vms` | Provides tasks to manage virtual machines hosted in Proxmox VE. | [View Documentation](../docs/roles/vms.md) |
| `vscode_server` | Install and configure Microsoft repository for VSCode. | [View Documentation](../docs/roles/vscode_server.md) |
| `wikipedia_setup` | Deploys and configures a Wikipedia instance using MediaWiki. | [View Documentation](../docs/roles/wikipedia_setup.md) |