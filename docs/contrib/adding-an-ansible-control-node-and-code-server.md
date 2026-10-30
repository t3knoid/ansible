# Adding an Ansible Control Node and Deploying code-server

This guide adds an existing, Ubuntu-installed, domain-joined VM as an Ansible control node, then deploys code-server to it and makes it reachable through HTTPS at a hostname such as `https://code.refol.us`.

The VM must already be reachable over SSH from the existing Ansible control node. This procedure does not install Ubuntu or join the VM to the domain. Run the deployment commands from the existing control node, which has this repository checked out and can reach the target, DNS services, certificate staging host, and reverse proxies as needed.

## 1. Prepare the Existing Control Node

On the existing control node, update the repository and activate its Ansible Python environment:

```bash
cd ~/ansible
git pull origin main
source /opt/python_3.12/bin/activate
INV=inventory/ansible/inventory.ini
HOST=ansible-2
DOMAIN=code.example.org
```

Change `HOST` and `DOMAIN` to the chosen host and hostname. The examples below use `inventory/ansible`; use a different inventory if that is where the VM and its services belong.

## 2. Add the VM to Inventory

Edit `inventory/ansible/inventory.ini` and add the host using the same connection conventions as neighboring hosts. For example, if it is managed as a Proxmox VM:

```ini
[vms]
ansible-2 ansible_host=192.168.20.103 vms_proxmox_node=pve-0

[code_server]
ansible-2
```

The example inventory defines `ansible` as a child of `vms`, and `python` as a child of `ansible`. A host in `vms` therefore also becomes an Ansible and Python host. If this VM is not managed through the `vms` group, add it to the appropriate control-node group instead and confirm the resulting group membership before deploying.

Add its unique IP address to `global_ip_addresses` in `roles/global/vars/main.yml`:

```yaml
global_ip_addresses:
  ansible-2: 192.168.20.103
```

Use the VM's actual reserved address and check that it is not already assigned. Set `ansible_host`, `ansible_user`, SSH options, and any host-specific connection variables according to the existing inventory pattern. Keep credentials and other secrets in the repository's vault or approved secret store, not in plaintext inventory.

Before continuing, inspect the inventory graph and test SSH/Ansible connectivity:

```bash
ansible-inventory -i "$INV" --graph
ansible -i "$INV" "$HOST" -m ping -e ansible_python_interpreter=/usr/bin/python3
```

Confirm that the target appears in `ansible`, `python`, and `code_server` as intended.

## 3. Bootstrap the Control Node

Run the existing control-node deployment against only the new VM:

```bash
ansible-playbook -i "$INV" playbooks/ansible/deploy_ansible.yml --limit "$HOST"
```

This playbook configures the Ansible node, creates the `/opt/python_<version>` environment, and installs the Ansible tooling. It expects the Ubuntu host to be reachable and already domain-joined as assumed above.

Verify the installed commands on the new control node, for example:

```bash
ssh "$HOST" '/opt/python_3.12/bin/ansible --version'
ssh "$HOST" '/opt/python_3.12/bin/ansible-lint --version'
```

Adjust the interpreter path if the inventory selects a different `python3_version`.

## 4. Set code-server and Proxy Variables

The `code_server` group selects hosts for `playbooks/deploy_code_server.yml`. Put service-specific settings in the inventory's `group_vars/code_server/main.yml` or a host-specific vars file, following the existing `inventory/ansible/group_vars/code_server/main.yml` example.

**Security recommendation: require OAuth2 authentication through Microsoft Entra ID for any code-server instance reachable beyond localhost.** Do not publish an unauthenticated code-server. This repository supports OAuth2 Proxy with Entra ID; use it for the external access path and keep its client secret and cookie secret in Ansible Vault or another approved secret store.

Set the code-server account and values required by the role, including `code_server_user` and `code_server_password`. The existing `inventory/ansible/group_vars/code_server/main.yml` uses `code_server_auth_mode: "none"` because the external reverse proxy enforces OAuth2. Only use that mode when the proxy is enforcing authentication and network controls prevent clients from bypassing the proxy to reach the code-server backend. Otherwise, retain code-server's password authentication as an additional layer.

Add a reverse-proxy site for the chosen hostname. Copy the structure of an existing site and adjust its hostname, backend, access policy, and authentication settings. In this repository, the code-server host runs a local Nginx frontend on port `8000`, which proxies to code-server bound to `127.0.0.1:8080`. The external reverse proxy should therefore target the code-server VM's address on port `8000`, not expose port `8080` directly.

For example, the site entry needs the equivalent of:

```yaml
rproxy_setup_sites:
  - server_name: code.example.org
    port: 8000
    proxy_pass: "http://192.168.20.103"
    enable: true
    use_oauth2: true
    use_entra_id_oidc: true
    oauth2_provider: "entra-id"
    oauth2_scope: "openid profile email"
    oauth2_callback_url: "https://code.example.org/oauth2/callback"
    oauth2_cookie_secret: "{{ vault_code_server_oauth2_cookie_secret }}"
    # Set access policy and any other site-specific fields from a neighboring site.
```

Use the real target IP or the repository's `global_ip_addresses` lookup convention. Add the host to the inventory's `[entra_id]` group as well as `[code_server]`; the OAuth2 deployment playbook reads site definitions from `entra_id`. The playbook creates or retrieves the Entra ID application and provisions its client secret. Configure the required Azure service-principal credentials and permissions using the repository's existing vault conventions. Do not copy client secrets or cookie secrets from another inventory.

## 5. Deploy code-server

Check syntax, then deploy to only the new host:

```bash
ansible-playbook -i "$INV" playbooks/deploy_code_server.yml --limit "$HOST" --syntax-check
ansible-playbook -i "$INV" playbooks/deploy_code_server.yml --limit "$HOST"
```

This playbook installs code-server and its local Nginx frontend. It does not configure the external reverse proxies, enforce Entra ID OAuth2, publish DNS records, or obtain a browser-trusted certificate.

## 6. Configure DNS, Certificates, and the External Proxy

For `https://code.example.org` to work, all of these must be true:

1. Public DNS for the hostname resolves to the public address of the external reverse proxy. Configure this at the authoritative DNS provider. A Pi-hole CNAME is only for clients using that internal DNS service; it does not publish a public DNS record.
2. If internal clients need a Pi-hole record, add a `pihole_cname_entries` item in the appropriate inventory vars, targeting the reverse proxy hostname, for example `code.example.org` to `rproxy-0.refol.us`. Follow the existing `pihole_cname_entries` pattern in `inventory/ansible/inventory.ini` and verify the DNS host in the selected inventory.
3. Generate and stage certificates from the selected inventory. Both certificate playbooks first run the `global` role on inventory hosts, then aggregate `rproxy_setup_sites` from hosts in the inventory passed with `-i`, flatten the lists, remove duplicate `server_name` entries, and display the resulting set. No separate `group_vars/certs` definition or CLI extra vars are required.

   **Scope:** these playbooks process every unique site found in the selected inventory, not only `$DOMAIN`. Check the displayed site list before proceeding. For example, `inventory/ansible/inventory.ini` currently contributes `code.refol.us`; an inventory with several service sites will request and stage certificates for all of them.

   ```bash
   ansible-playbook -i "$INV" playbooks/certs/generate_certs.yml
   ansible-playbook -i "$INV" playbooks/certs/stage_certs.yml
   ```

   The certificate role uses Certbot `--force-renewal` for each aggregated site, so avoid repeated production runs and review the list to avoid unnecessary requests. Ensure DNS and the ACME challenge path are ready, and set `certs_email` to a monitored address when appropriate. For an ACME test, set `certs_staging: true` for the cert hosts; staging certificates are not browser-trusted. Remove that setting and generate production certificates before staging them for service.

4. Deploy the Entra ID OAuth2 Proxy configuration:

   ```bash
   ansible-playbook -i "$INV" playbooks/oauth2_proxy/deploy_oauth2_proxy.yml --syntax-check
   ansible-playbook -i "$INV" playbooks/oauth2_proxy/deploy_oauth2_proxy.yml
   ```

   This playbook aggregates site definitions from every host in `[entra_id]`, registers or retrieves Entra ID applications, and configures OAuth2 Proxy on the host in `[oauth2_proxy]`. Review the complete inventory-wide set of affected sites before running it. It is not a single-host deployment; limiting it can omit other sites from the generated configuration.

5. Configure the external reverse proxies from the inventory site definition:

   ```bash
   ansible-playbook -i "$INV" playbooks/rproxy/config_rproxy.yml --syntax-check
   ansible-playbook -i "$INV" playbooks/rproxy/config_rproxy.yml
   ```

   `playbooks/rproxy/config_rproxy.yml` aggregates `rproxy_setup_sites` from the inventory and configures each host in the `rproxy` group. The reverse-proxy role can create a self-signed certificate when no certificate is staged; that is not browser-trusted HTTPS. Confirm the valid certificate is in place before declaring the public URL ready. Verify an unauthenticated request is redirected to Entra ID and that access is denied unless authentication succeeds.

## 7. Validate the Result

Check DNS from both an internal client and, where applicable, an external network. Then verify HTTPS and the application response:

```bash
dig +short "$DOMAIN"
curl -I "https://$DOMAIN"
```

A redirect or authentication response can be expected, depending on the configured proxy policy. Confirm that the TLS certificate is trusted and issued for the chosen hostname, and then sign in through the configured authentication path.

## Inventory Checklist

- The existing VM is reachable over SSH and already has Ubuntu and domain membership.
- The host is in the required `ansible`, `python`, and `code_server` inventory groups.
- Proxmox membership and VM variables are present only when the VM is managed by the repository's `vms` workflow.
- The host's address is unique in `roles/global/vars/main.yml`.
- `code_server_user`, authentication, and any required secrets are defined securely.
- A reverse-proxy site targets the code-server host on port `8000` and has an intentional access policy.
- Public DNS, optional Pi-hole DNS, and a valid staged TLS certificate point to the external reverse proxy.
- Inventory graph, connectivity, syntax checks, and final HTTPS access have been verified.
