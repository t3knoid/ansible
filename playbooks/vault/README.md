# 📚 Playbooks in `vault`

| Playbook | Purpose |
|----------|---------|
| [`config.yml`](config.md) | Configures HashiCorp Vault on designated vault servers. |
| [`create_ca.yml`](create_ca.md) | Creates a Certificate Authority and Vault server certificate for HashiCorp Vault. |
| [`create_vault_cert.yml`](create_vault_cert.md) | Creates a Vault server certificate using an existing Certificate Authority for HashiCorp Vault. |
| [`deploy_cacert_to_clients.yml`](deploy_cacert_to_clients.md) | Deploys the Vault CA public certificate to all Vault client machines. |
| [`deploy_vault.yml`](deploy_vault.md) | Deploys HashiCorp Vault including installation, CA creation, server certificate creation, configuration, and CA certificate deployment to clients. |
| [`install.yml`](install.md) | Installs HashiCorp Vault on designated vault servers. |
| [`remove_vault.yml`](remove_vault.md) | Removes HashiCorp Vault from designated vault servers. |