certs
======

The certs role uses [certbot](https://certbot.eff.org/instructions?ws=nginx&os=pip) to create certificates.

Requirements
------------

This role requires the nginx and certbot roles to be deployed on the target host.

Role variables
--------------

- certs_rsa_key_size: 4096
- certs_email: "" # Adding a valid address is strongly recommended
- certs_staging: 1 # Set to 1 if you're testing your setup to avoid hitting request limits
- certs_home: /data/letsencrypt

In order to create certificate, make sure to set the certs_staging to 0. Use the -e option on the ansible-playbook command-line.

```bash
ansible-playbook -i $INV playbooks/generate_certs.yml -e "certs_staging=0" -k
```

Dependencies
------------

None

Example Playbook
----------------

The following will generate certificates in the target node.

    gather_facts: false
      become: true
      roles:
        - global
        - certs


