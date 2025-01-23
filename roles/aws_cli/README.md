aws_cli
======

The aws_cli role is used to install and configure AWS CLI.

Requirements
------------

None

Role variables
--------------

- aws_cli_user - terraform-svc
- aws_cli_region - "us-west-2"
- aws_cli_output - "json"
- aws_cli_access_key - Defined in vars/main/vault.yml
- aws_cli_access_key_secret - Defined in vars/main/vault.yml

Dependencies
------------

None

Example Playbook
----------------

The following playbook installs and configures AWS CLI.

      - name: Deploy AWS CLI
        hosts: all
        become: true
        roles:
          - aws_cli

