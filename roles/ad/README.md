ad
=========

Provides tasks to manage joining and leaving an active directory domain.

Requirements
------------

Requires the *global* role.

Role Variables
--------------

- ad_required_packages - lists required packages in order to join an active directory domain.
- ad_additional_packages - list any other additional packages. This is typically empty. This is only here for any future changes.
- ad_administrator_password - The active directory domain Administrator (i.e. Administrator) password.

Dependencies
------------

- global_domain_name - Domain name defined in *global* role.

Example Playbook
----------------

The following shows a playbook to join an active directory domain.

    - name: Join active directory domain
      hosts: all
      gather_facts: false
      become: true
      roles:
        - global
      tasks:
        - name: Import ad role
          ansible.builtin.import_role:
          name: ad
