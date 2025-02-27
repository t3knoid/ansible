certs
======

The certs role uses [certbot](https://certbot.eff.org/instructions?ws=nginx&os=pip) to create certificates.

Requirements
------------

This role requires the nginx and certbot roles to be deployed on the target host. A minimum playbook must include the global role to execute prior to the certs role. Ensure that there are A or CNAME records for server_names defined in the global/defaults/main/sites.yml. 

Role variables
--------------

- certs_rsa_key_size: 4096
- certs_email: "" # Adding a valid address is strongly recommended
- certs_staging: 1 # Set to 1 if you're testing your setup to avoid hitting request limits
- certs_home: /data/letsencrypt

In order to create certificate, make sure to set the certs_staging to false.

```bash
ansible-playbook -i $INV playbooks/certs/generate_certs.yml -k
```

To stage the generated certificates to the staging folder with the nginx server configurations expects them, execute the following command.
```bash
ansible-playbook -i $INV playbooks/certs/stage_certs.yml -k
```

Dependencies
------------

This role depends on the certbot and nginx roles applied to the target host (i.e., [certbot] inventory group).

The inventory file must define the certs group which would contain the location of the certificates. 

[certs]
rproxy-0 

Example Playbook
----------------

The following will generate certificates in the target node.

    gather_facts: false
      become: true
      roles:
        - global
        - certs


