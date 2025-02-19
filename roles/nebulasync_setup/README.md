nebulasync_setup
=========

Installs nebula-sync as documented in its [GitHub page](https://github.com/lovelaze/nebula-sync?tab=readme-ov-file#installation).

Requirements
------------

This role requires that pi-hole role is configured on the target host. The target host is assumed to be the first host listed in the "primary_dns" inventory group.

Role Variables
--------------

- nebulasync_setup_version - the version of nebula-sync to download and install
- nebulasync_setup_installdir - the folder where to install nebula-sync, it defaults to "/usr/local/bin"
- nebulasync_setup_envfilepath - the path to a text file containing nebula-sync configuration variables, it defaults to "/etc/nebula-sync.env"
- nebulasync_setup_primary -s ets the primary DNS by enumerating the first entry of the "primary_dns" inventory group
- nebulasync_setup_replicas -s ets the DNS replica, it currently sets the first entry of the "secondary_dns" inventory group (future implementation will support a list of replicas)
- nebulasync_setup_settings - a dictionary of nebulasync-settings.

Dependencies
------------

nebula-sync requires that Python is installed.

Example Playbook
----------------

    - name: Deploy nebula-sync
      hosts: primary_dns
      gather_facts: true
      roles:
        - global
        - nebulasync_setup
