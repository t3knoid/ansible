# Configure An Inventory Host Web Service For A Reverse Proxy

This runbook explains how to update an inventory so a host web service is available through the repository's reverse proxy setup.

## Scope

This runbook covers required updates in:

- `inventory/<inventory_name>/inventory.ini`
- `inventory/<inventory_name>/host_vars/<service_host>.yml` or the inventory's existing shared vars file
- `roles/global/vars/main.yml` when the service host does not already have an IP address entry

It also includes the required DNS deployment, certificate generation, and certificate staging steps.

## Prerequisites

- The web service is running and reachable from the backend proxy hosts on its configured port.
- The reverse proxy hosts are provisioned and accessible over SSH with privilege escalation.
- Pi-hole connection values and credentials used by the DNS playbooks are already configured in global vars/vault.
- Public DNS for the site points to the frontend, directly or through the existing Cloudflare configuration. The Pi-hole CNAME configures local DNS; it does not create public DNS records.
- The certificate host has certbot and its nginx plugin installed. Public DNS and HTTP access to the ACME challenge endpoint must allow Let's Encrypt validation.
- Firewall rules allow HTTPS traffic to the frontend, HTTP traffic from the frontend to the backend proxies, and traffic from the backend proxies to the service port.

Traffic follows this path:

```text
Client -> rproxy-0:443 -> rproxy-1:80 (or rproxy-2:80) -> service_host:service_port
```

## 1) Update Inventory Host Groups And CNAME Entries

Edit `inventory/<inventory_name>/inventory.ini` and set `pihole_cname_entries` on the target service host. Use the site's public name as `domain` and the frontend proxy's DNS name as `target`.

Example:

```ini
[baremetal]
ecube-2 pihole_cname_entries='[{"domain": "rosie.refol.us", "target": "rproxy-0.refol.us"}]'

[cname]
ecube-2
```

Both the host variable and `[cname]` membership are required. The DNS playbook selects hosts in `cname` and reads their `pihole_cname_entries` values.

Keep the host in its existing application and infrastructure groups. For a VM, set the variable on its existing entry under `[vms]` instead of adding it to `[baremetal]`.

Also ensure the reverse proxy and certificate groups are defined:

```ini
[rproxy_main]
rproxy-0

[rproxy_primary]
rproxy-1

[rproxy_secondary]
rproxy-2

[rproxy:children]
rproxy_main
rproxy_primary
rproxy_secondary

[certs]
rproxy-0
```

Notes:

- `rproxy_main` contains the HTTPS frontend.
- `rproxy_primary` and `rproxy_secondary` contain the backend proxies. The default upstream configuration uses the first host in each group.
- `certs` selects the host where certificates are generated and staged. In this example, it is the frontend that serves HTTPS.
- `playbooks/rproxy/config_rproxy.yml` selects service hosts in `vms` or `baremetal` and deploys their site definitions to every host in `rproxy`.

## 2) Verify The Service Host IP Address

Edit `roles/global/vars/main.yml` and verify `global_ip_addresses` contains the service host.

Example of an existing entry:

```yaml
global_ip_addresses:
  ecube-2: 192.168.90.196
```

Keep the rest of the map intact. For a new host, add an available address in the appropriate subnet and verify it is not already assigned. Do not change an existing host's address just to match this example.

## 3) Update The Inventory Site Configuration

For a host-specific site, edit `inventory/<inventory_name>/host_vars/<service_host>.yml`. If the inventory already defines sites in shared vars, update that list instead.

Example:

```yaml
rproxy_setup_sites:
  - server_name: rosie.refol.us
    port: 8000
    proxy_pass: "http://{{ global_ip_addresses['ecube-2'] }}"
    allow_list:
      - 192.168.0.0/24
      - 192.168.2.0/24
    restricted: false
    use_oauth2: false
    enable: true
```

Settings:

| Setting | Values | Default | Setting Description |
| --- | --- | --- | --- |
| `pihole_cname_entries` | List of `domain` and `target` mappings | Required for CNAME deployment | Host variable in the inventory file. Maps the site name to the frontend proxy's DNS name. |
| `rproxy_setup_sites` | List of site mappings | Required for selected service hosts | Defines the sites to deploy. |
| `server_name` | Site DNS name | Required | Must match the CNAME domain, client-facing URL, and TLS certificate. |
| `port` | Service listening port | Required | Port reached by the backend proxies. |
| `proxy_pass` | Upstream URL without the service port | Required | Service address, including `http://` or `https://`. The template appends `:<port>`. |
| `allow_list` | IP addresses or CIDR ranges | Required when `restricted: true`; otherwise unused | Additional frontend allow rules. The template also includes built-in LAN allow rules. |
| `restricted` | `true`, `false` | `false` | Enables frontend IP restrictions and HTTP Basic authentication using the existing `.htpasswd` file. |
| `use_oauth2` | `true`, `false` | `false` when omitted by the configuration task | Enables the separate OAuth2 integration. Leave disabled for this runbook. |
| `enable` | `true`, `false` | Set explicitly | Creates or removes the site's `sites-enabled` link. |
| `rproxy_setup_cloudflare_only` | `true`, `false` | `true` | Role-level frontend restriction to Cloudflare and built-in LAN ranges, separate from `restricted`. |
| `certs_staging` | `true`, `false` | `false` | Uses the Let's Encrypt staging service when enabled. Staging certificates are not publicly trusted. |
| `certs_home` | Directory path | `/data/letsencrypt` | Certbot certificate storage on the certificate host. |
| `certs_stage` | Directory path | `/data/certs` | Destination for staged certificate files used by nginx in the default configuration. |

Notes:

- Do not include the service port in both `proxy_pass` and `port`.
- A host vars list overrides an inherited list; it does not append to it. Keep all sites needed by that host in the effective list.
- Avoid defining the same `server_name` on multiple selected hosts, including through shared vars.
- Configure the application's external URL as `https://<server_name>` when required. Follow the service role's existing settings for trusted proxies, forwarded headers, and backend TLS.
- `restricted: false` does not disable the role's Cloudflare-only restriction.

## 4) Deploy DNS And Reverse Proxy Changes

Deploy the target host's CNAME entries:

```bash
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/dns/add_cname_entry.yml --limit <service_host> -u ansible
```

For the example above, replace `<service_host>` with `ecube-2`.

If the proxy infrastructure has not already been set up, run:

```bash
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/rproxy/deploy_rproxy.yml -u ansible
```

Deploy the selected host's site configuration to every reverse proxy:

```bash
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/rproxy/config_rproxy.yml --limit <service_host> -u ansible
```

Notes:

- `deploy_rproxy.yml` configures proxy infrastructure. `config_rproxy.yml` deploys the service site definitions and enables the sites.
- Limit site configuration to the service host, not a proxy hostname. The role delegates configuration to the proxy hosts.
- Site configuration creates a self-signed certificate when no certificate exists. Complete the next step to generate and stage a trusted certificate.

## 5) Generate And Stage The Certificate

Generate certificates using the target inventory, then stage them for nginx:

```bash
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/certs/generate_certs.yml -u ansible
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/certs/stage_certs.yml -u ansible
```

Notes:

- These playbooks collect `rproxy_setup_sites` from the inventory and run certificate tasks on the hosts in `certs`. Do not reuse the service-host `--limit` from the previous step; that would exclude the certificate host.
- Generation requests Let's Encrypt certificates for the inventory's site names. It uses `--force-renewal`, so avoid unnecessary repeated runs and account for issuance rate limits.
- Staging copies `cert.pem`, `fullchain.pem`, and `privkey.pem` from certbot storage to the site's directory under `certs_stage` and restarts nginx when files change.
- Generation alone does not install the certificate in nginx's configured certificate path. Both commands are required.
- The generation role ignores certbot task failures. Check each site's result and confirm the issued certificate exists before staging.

## 6) Validate

Inventory and host selection checks:

```bash
ansible-inventory -i inventory/<inventory_name>/inventory.ini --graph cname
ansible-inventory -i inventory/<inventory_name>/inventory.ini --graph rproxy
ansible-inventory -i inventory/<inventory_name>/inventory.ini --graph certs
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/rproxy/config_rproxy.yml --limit <service_host> --list-hosts
ansible-playbook -i inventory/<inventory_name>/inventory.ini playbooks/rproxy/config_rproxy.yml --syntax-check
```

Run nginx validation on all proxy hosts:

```bash
ansible rproxy -i inventory/<inventory_name>/inventory.ini -m ansible.builtin.command -a 'nginx -t' -b -u ansible
```

From a client using Pi-hole, verify the local CNAME. From an allowed client network, check HTTPS:

```bash
dig <server_name> CNAME
curl -I https://<server_name>
```

Behavior checks:

- The local CNAME points to the frontend proxy's DNS name, and that name resolves to the intended proxy address.
- Accessing `https://<server_name>` reaches the intended application and presents a trusted certificate for that name.
- The frontend has `fullchain.pem` and `privkey.pem` under `/data/certs/<server_name>/` with the default paths.
- The site configuration exists in `/data/nginx/sites-available/` and is linked in `/data/nginx/sites-enabled/` on every proxy when `enable: true`.
- Application links, redirects, and WebSocket connections work through the public URL when used by the service.

## Troubleshooting

- CNAME not created: verify the target host is in `cname`, its `pihole_cname_entries` value is set, and the DNS deployment selected that host.
- No hosts matched or no site deployed: verify the service host is in `vms` or `baremetal`, has an effective `rproxy_setup_sites` list, and is not excluded by `--limit`.
- Default site or wrong application: verify DNS, `server_name`, enabled site links on every proxy, and duplicate site definitions.
- 502/504 response: verify backend proxies can reach the service address and port, the service listens beyond localhost, and the frontend can reach the backend proxies on port 80.
- 403 response: verify the frontend's Cloudflare-only policy, built-in LAN ranges, site restrictions, and nginx logs. The template also blocks selected chatbot user agents.
- 401 response: verify whether `restricted: true` enabled Basic authentication and whether the existing `.htpasswd` credentials are configured.
- Certificate generation failed: verify `certs` membership, public DNS, certbot availability, and external access to the HTTP ACME challenge endpoint. Inspect the certbot output even if the play completes.
- Certificate warning: verify generation and staging both completed, `certs_staging` is false for production issuance, and nginx serves the trusted certificate for the exact `server_name`.
- Redirect loop or incorrect links: verify the application's external URL, trusted proxy settings, and forwarded headers across both proxy layers.