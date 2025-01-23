disks
======

The disks role installs and configures code server.

Requirements
------------

Requires the users role.

Role variables
--------------

- disks_disk_mounts - defines a list of dictionary defining the disk mountpoint, owner, and group.

Dependencies
------------

None

Example Playbook
----------------

The following playbok prepares an attached disk.

    - name: Automate finding and formatting a local drive
      hosts: all
      gather_facts: true
      become: true
      roles:
        - users
        - disks
