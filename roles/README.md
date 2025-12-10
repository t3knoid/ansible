# 📚 Role Index

- [`ad`](ad/README.md): Installs the required packages in order for a node to join an active directory domain. Use the user ansible (e.g. -u ansible) when using this role

- [`ansible_node`](ansible_node/README.md): Configures a node to be used as an Ansible control node.
- [`ansible_setup`](ansible_setup/README.md): Provides tasks to install and configure Ansible on a control node.
- [`autofs`](autofs/README.md): Installs and configures autofs on Debian/Ubuntu.
- [`aws_cli`](aws_cli/README.md): Installs and configures AWS CLI.
- [`azure_cli_setup`](azure_cli_setup/README.md): Installs Microsoft Azure CLI
- [`azure_ps_setup`](azure_ps_setup/README.md): Installs Microsoft Azure PowerShell
- [`bedrock_setup`](bedrock_setup/README.md): Installs Minecraft Bedrock Server on Linux systems.
- [`calibre_setup`](calibre_setup/README.md): Installs and configures Calibre eBook management software. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre).

- [`calibreweb_setup`](calibreweb_setup/README.md): Installs and configures Calibre-Web, a web-based eBook management application. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/calibre-web).

- [`certbot_setup`](certbot_setup/README.md): It deploys certbot following instructions documented in https://certbot.eff.org/instructions?ws=nginx&os=pip. Target hosts must be in a group named *[certbot]* in its inventory. Certbot is used to obtain SSL/TLS certificates from Let's Encrypt.

- [`certs`](certs/README.md): Provides tasks to request and renew SSL/TLS certificates from Let's Encrypt. It also provides tasks to stage certificates for eventual use by the Nginx reverse proxy and other services.

- [`cloudinit`](cloudinit/README.md): Provides tasks to create a virtual machine with cloud-init support.
- [`code_server`](code_server/README.md): Installs and configures code server.
- [`disks`](disks/README.md): Prepares an attached disk by formatting and mounting to a defined mountpoint. Removes mounts from fstab that is associated with a none existing device.

- [`docker_setup`](docker_setup/README.md): Installs Docker and Docker Compose on Debian/Ubuntu systems.
- [`elasticsearch_setup`](elasticsearch_setup/README.md): Install and configure Elasticsearch on Debian/Ubuntu
- [`entra_id_oauth2`](entra_id_oauth2/README.md): Configures entra_id settings for oAuth2-enabled sites.
- [`geyser_setup`](geyser_setup/README.md): Installs and configures GeyserMC on Debian/Ubuntu systems as documented at https://geysermc.org/wiki/geyser/setup/?host=self&platform=standalone

- [`global`](global/README.md): Provides global defaults common to all roles. It provides the IP definition of each host in the datacenter. Every host must be defined here with its corresponding IP address. Other global variables are also defined here.

- [`grafana_setup`](grafana_setup/README.md): Install and configure Grafana on Debian/Ubuntu
- [`graphite_setup`](graphite_setup/README.md): Installs and configures Graphite on Debian/Ubuntu systems.
- [`java_setup`](java_setup/README.md): Installs and configures Java on Debian/Ubuntu systems.
- [`jenkins_setup`](jenkins_setup/README.md): Installs and configures Jenkins on Debian/Ubuntu systems.
- [`lamp_setup`](lamp_setup/README.md): Install and configure LAMP on Debian/Ubuntu.
- [`lazylibrarian_setup`](lazylibrarian_setup/README.md): Installs and configures LazyLibrarian on Debian/Ubuntu systems. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lazylibrarian).

- [`lidarr_setup`](lidarr_setup/README.md): Installs and configures Lidarr on Debian/Ubuntu systems. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/lidarr).

- [`linux_updates`](linux_updates/README.md): The linux role contains tasks related to updating Linux updates.
- [`mediawiki_setup`](mediawiki_setup/README.md): Installs and configures MediaWiki on Ubuntu systems.
- [`minecraft_setup`](minecraft_setup/README.md): Installs Minecraft Server on Ubuntu and Debian systems (https://www.minecraft.net/en-us/download/server).

- [`mongodb_setup`](mongodb_setup/README.md): Installs [MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/).
- [`nebulasync_setup`](nebulasync_setup/README.md): Installs nebula-sync as documented in its [GitHub page](https://github.com/lovelaze/nebula-sync?tab=readme-ov-file#installation). This role requires that pi-hole role is configured on the target host. The target host is assumed to be the first host listed in the "primary_dns" inventory group.

- [`nginx_setup`](nginx_setup/README.md): Installs the nginx service.
- [`node_exporter_setup`](node_exporter_setup/README.md): Installs Prometheus Node Exporter
- [`oauth2_proxy_setup`](oauth2_proxy_setup/README.md): Install and configure OAuth2 Proxy.
- [`oc_setup`](oc_setup/README.md): Install and configure TP-Link Omada Controller on Ubuntu systems.
- [`ombi_setup`](ombi_setup/README.md): Ombi Setup installs and configures an Ombi Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/ombi)

- [`pbs`](pbs/README.md): Installs and configures Proxmox Backup Server on Ubuntu systems.
- [`pihole`](pihole/README.md): Installs and configures Pi-hole on Ubuntu systems (https://pi-hole.net/). Provides tasks to manage Pi-hole settings and configurations.

- [`playwright`](playwright/README.md): Installs playwright.
- [`pve`](pve/README.md): Contains tasks to manage the Proxmox Virtual Environment
- [`pxeserver_setup`](pxeserver_setup/README.md): The pxeserver_setup role is used to install and configure a [PXE server](https://ubuntu.com/server/docs/how-to-netboot-the-server-installer-on-amd64). For this to work under TP-Link Omada router, enable the "Legal DHCP Servers" setting and set it to the PXE server IP address.

- [`python3`](python3/README.md): Installs Python 3 from the Python Software Foundation (PSF) repository. There is also an alternate option is to compile Python 3 from source.

- [`radarr_setup`](radarr_setup/README.md): Installs and configures a Radarr Docker container. It uses an image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/radarr).

- [`redis_setup`](redis_setup/README.md): Installs and configures Redis.
- [`redmine_setup`](redmine_setup/README.md): Redmine Setup installs and configures an [Redmine](https://www.redmine.org/). The installation instructions are taken directly from [Redmine's installation guide](https://www.redmine.org/projects/redmine/wiki/RedmineInstall) and adapting [redmineadvisor.com's instructions](https://www.redmineadvisor.com/articles/6_0/install/ubuntu24/) on installing Redmine in Ubuntu 24.

- [`rproxy_setup`](rproxy_setup/README.md): rproxy_setup configures reverse proxy with failover support using nginx. This role requires at least three hosts to be defined. One host is configure as the main frontend proxy, the other two acts as the primary and secondary proxy.

- [`ruby_setup`](ruby_setup/README.md): The ruby_setup role builds and install Ruby from it's [https://www.ruby-lang.org/en/downloads/](source code).

- [`sabnzbd_setup`](sabnzbd_setup/README.md): Installs and configures a Sabnzbd Docker container. It uses a Docker image distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sabnzbd).

- [`semaphoreui_setup`](semaphoreui_setup/README.md): Installs and configures [Semaphore UI](https://docs.semaphoreui.com/).
- [`sonarr_setup`](sonarr_setup/README.md): Installs and configures a Sonarr Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/sonarr).

- [`sshpass`](sshpass/README.md): Installs sshpass from apt repositories.
- [`synology`](synology/README.md): Provides tasks to manage Synology NAS devices.
- [`tautulli_setup`](tautulli_setup/README.md): Installs and configures an Tautulli Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/tautulli).

- [`terraform_setup`](terraform_setup/README.md): Installs Terraform
- [`users`](users/README.md): Provides tasks to manage system users in Ubuntu and Debian.
- [`vault_setup`](vault_setup/README.md): Installs and configures Hashicorp Vault
- [`vms`](vms/README.md): Provides tasks to manage virtual machines hosted in Proxmox VE.
- [`vscode_server`](vscode_server/README.md): Install and configure Microsoft repository for VSCode.
- [`wikipedia_setup`](wikipedia_setup/README.md): Deploys and configures a Wikipedia instance using MediaWiki.