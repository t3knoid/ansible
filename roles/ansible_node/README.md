ansible_node
=========

Configures host as an ansible managed node. It ensures that the ansible group exists and is added to the sudoers group.

Requirements
------------

Requires the global role. Must be executed with elevation.

Role Variables
--------------

None

Dependencies
------------

None

Example Playbook
----------------

The following playbook calls the ansible_role to prepare the target host for management by Ansible.

        - name: Prepare ansible managed node
            hosts: all
            gather_facts: true
            become: true
            roles:
              - ansible_node
