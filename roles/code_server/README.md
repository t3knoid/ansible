code_server
======

The code_server role installs and configures code server.

Requirements
------------

None

Role variables
--------------

- code_server_version - "4.95.2"

Dependencies
------------

None

Example Playbook
----------------

The following playbok installs and configures code server.

      - name: Install and configure code-server
        hosts: all
        become: true
        gather_facts: true
        roles:
          - global
          - code_server

