semaphoreui_setup
=========

Installs and configures [Semaphore UI](https://docs.semaphoreui.com/).

Requirements
------------

This role requires a Postgresql database.

Role Variables
--------------

- semaphoreui_setup_version - The version of Semaphore UI to install
- semaphoreui_setup_python_packages - A list of Python packages required by Ansible
- semaphoreui_setup_homedir: Semaphore home directory
- semaphoreui_setup_tmpdir: Semaphore temp folder
- semaphoreui_setup_etcdir: Semaphore configuration folder
- semaphoreui_setup_pgdb_ip: IP address of the Postgres database host
- semaphoreui_setup_pgclient_ip: IP address of the Postgres client

The following are in the vault.yml file.

- semaphoreui_setup_db_name: Semaphore database name
- semaphoreui_setup_db_user: Semaphore database username
- semaphoreui_setup_db_password: Semaphore database password
- semaphoreui_setup_admin: Semaphore admin user login
- semaphoreui_setup_admin_pw: Semaphore admin user password
- semaphoreui_setup_admin_email: Semaphore admin user email address
- semaphoreui_setup_admin_name: Semaphore admin's give name

Dependencies
------------

This depends on the postgresql_setup role.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: semaphore
      roles:
         - semaphoreui_setup
