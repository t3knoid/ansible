linux_updates
=========

The linux role contains tasks related to updating Linux updates.

Requirements
------------

None

Role Variables
--------------

None

Dependencies
------------

None

Example Playbook
----------------

- hosts: vms,linux
  become: true
  roles:
    - linux_updates

