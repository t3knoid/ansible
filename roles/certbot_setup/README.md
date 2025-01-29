certbot
======

The certbot role creates deploys [certbot](https://certbot.eff.org/instructions?ws=nginx&os=pip).

Requirements
------------

This role requires the Python environment configured in /opt/certbot. Target hosts must be in a group named *[certbot]* in its inventory.

Role variables
--------------

none

Dependencies
------------

None

Example Playbook
----------------

The following playbook deploys certbot to the target host.

    - name: Deploy certbot
      hosts: certbot
      become: true
      roles:
        - global
        - users
        - python3
        - certbot_setup


