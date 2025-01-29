docker_setup
======

The docker_setup role uses deploys Docker and docker-compose.

Requirements
------------

None

Role variables
--------------

- docker_setup_containerd_version: 1.7.24-1
- docker_setup_docker_ce_version: 27.3.1-1
- docker_setup_buildx_plugin_version: 0.17.1-1
- docker_setup_docker_compose_plugin_version: 2.29.7-1
- docker_setup_arch: amd64
- docker_setup_distro: noble
- docker_setup_download_root: "https://download.docker.com/linux/ubuntu/dists"
- docker_setup_packages - list of Docker packages to install
- docker_setup_compose_version - version of docker-compose to install

Dependencies
------------

None

Example Playbook
----------------

The following isntalls Docker on the target node.

    - name: Install Docker
      hosts: docker
      become: true
      gather_facts: false
      roles:
        - global
        - users
        - docker_setup
