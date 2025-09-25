ansible_setup
=============

Installs and configures Ansible.

Requirements
------------

Requires the *global* role.

Role Variables
--------------

ansible_setup_ver: The version of ansible to install
ansible_setup_callback_plugins: A list of callback plugins to install
ansible_setup_workdir: Ansible work directory location, "/ansible/dev/ansible"
ansible_setup_config_path: ansible.cfg file path
ansible_setup_python_modules: Python modules to install

Dependencies
------------

None

Example Playbook
----------------

The following playbook deploys Ansible to a given host.

      - name: Deploy ansible
        hosts: all
        gather_facts: false
        become: true
        become_user: root
        roles:
          - global
          - ansible_setup

