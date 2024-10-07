Role Name
=========

This role creates VMs using Proxmox VE. It primarily uses the following collection.

https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html
https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_nic_module.html
https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_disk_module.html
https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_vm_info_module.html
[community.general.proxmox_template module](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_template_module.html)

Autoinstall

https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html


Requirements
------------

The kvm_module requires the following Python modules:
- proxmoxer
- requests

```bash
python -m pip install proxmoxer
python -m pip install requests
```

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
