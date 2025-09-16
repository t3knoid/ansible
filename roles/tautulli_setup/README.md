Tautulli Setup
----------

Tautulli Setup installs and configures an Tautulli Docker container. It uses a container distributed by [linuxserver](https://hub.docker.com/r/linuxserver/tautulli)

Requirements
------------

This role requires the following roles:

- global
- users
- docker_setup

Initial Deploy
--------------

``` shell
INV=inventory/tautulli/inventory.ini
ansible-playbook -k -u ansible -i $INV playbooks/provision_vm.yml
ansible-playbook -k -u ansible -i $INV playbooks/tautulli/deploy_tautulli.yml
ansible-playbook -k -i $INV playbooks/certs/generate_certs.yml
ansible-playbook -k -i $INV playbooks/certs/stage_certs.yml
ansible-playbook -k -i $INV playbooks/rproxy/config_rproxy.yml
ansible-playbook -k -i $INV playbooks/dns/add_cname_entry.yml
```