# 📚 Playbooks in `certs`

| Playbook | Purpose |
|----------|---------|
| [`distribute_pve_certs.yml`](distribute_pve_certs.md) | Distribute web certificates from cert staging host to Proxmox nodes |
| [`generate_certs.yml`](generate_certs.md) | Generate Let’s Encrypt certbot certificates on the cert staging host |
| [`stage_certs.yml`](stage_certs.md) | Stage certificates on the cert staging host in preparation for use by reverse proxy and other services |