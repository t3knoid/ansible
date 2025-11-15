# vault_setup role

The vault_setup role contains task to install and configure the HashiCorp Vault. This vault will be used to store secrets for Ansible and Terraform.

## Vault installation

The vault is deployed to the server and client hosts. An Ansible playbook is used to install and configure the vault server.

### Ansible Playbook

Configure the target inventory with the following groups:

[vault_servers]
dns-1

[vault_clients]
ansible-0

As what each name suggests, vault_servers defines the vault server hosts and vault_clients defines the vault client hosts. In the above example, the vault server is installed in the dns-1 host and ansible-0 is a client.

``` bash
INV=inventory/ansible/inventory.ini
ansible-playbook -k -i $INV playbooks/vault/deploy_vault.yml
```

This orchestrates the deployment and configuration of Vault to the server and client hosts, as well as, creates the certificate authority and server certificates.

### Certificate Authority

A Certificate Authority (CA) is like a trusted “signer” that issues certificates. It signs the certificate that the server uses to identify itself to the clients (see vault certificate in the following paragraph). The *roles/vault_setup/tasks/create_ca.yml* task file contains tasks that creates the certificate authority. This creates a certificate, */etc/vault.d/ca.crt*, in the vault server host. This certificate is deployed to clients in order to validate the vault server certificate.

### Vault Server Certificate

A vault certificate is created in the vault server and signed by the certificate authority. This certificate is used to identify the vault server to clients. It is what allows the clients to "trust" the server. The *roles/vault_setup/tasks/create_vault_cert.yml* contains the tasks that creates this certificate.

### Configuring the Vault Server

After the server certificates have been created, the vault server is configured using the tasks in roles/vault_setup/tasks/config.yml file. It modifies the /etc/vault.d/vault.hcl with appropriate settings.

### CA Certificate Deploy to Clients 

Vault clients are required to have the CA certificate installed. The CA certificate is what allows the client to trust the server it is connecting to. The *roles/vault_setup/tasks/deploy_cacert_to_clients.yml* file contains tasks that copies the ca.crt file from the server to the clients.

## Connecting Clients to the Server

Configure Vault clients by setting the **VAULT_ADDR** environment variable from the terminal as shown here.

```bash
export VAULT_ADDR="https://vault.refol.us:8200"
```

Note that the above hostname is an alias to dns-0.

Finally, test the connection to the vault by executing the following.

```bash
vault status
```

This should output something similar to the following.

```bash
Key                Value
---                -----
Seal Type          shamir
Initialized        false
Sealed             true
Total Shares       0
Threshold          0
Unseal Progress    0/0
Unseal Nonce       n/a
Version            1.21.0
Build Date         2025-10-21T19:33:18Z
Storage Type       file
HA Enabled         false
```
