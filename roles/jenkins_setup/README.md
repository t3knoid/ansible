jenkins_setup
=========

The jenkins_setup role installs and configures Jenkins.

Requirements
------------


Role Variables
--------------

- jenkins_setup_version - the versions of Jenkins to install
- jenkins_setup_war - download URL of the jenkins WAR file
- jenkins_setup_home - location of Jenkins configuration and work files
- jenkins_setup_repo_key_url - repo key URL
- jenkins_setup_repo_key_local - repo key local file 

Dependencies
------------

Jenkins requires the global and java roles.


Example Playbook
----------------

    - name: Deploy Jenkins
      hosts: jenkins
      become: true

      roles:
        - global
        - java_setup
        - jenkins_setup


License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
