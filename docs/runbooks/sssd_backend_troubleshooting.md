# SSSD Backend Troubleshooting

Use this runbook to diagnose an SSSD (System Security Services Daemon) domain reporting `Backend is offline` on Ubuntu. Work from network reachability through DNS, transport, TLS where configured, Kerberos, and finally cached state. Log messages are clues, not unique diagnoses; an active daemon or a cached identity lookup does not prove the backend is online.

Run commands individually on the affected guest unless noted otherwise. Do not execute this document as a script. Keep a tested local administrator/root console session open before changing authentication, restarting SSSD, or removing caches. Obtain approval for disruptive changes and preserve relevant logs before resetting state. Never share passwords, keytab contents, credential caches, or unredacted debug logs.

## 1. Establish Scope and Recovery Access

Record the Ubuntu and SSSD versions, affected users/domains, onset time, and recent network, DNS, certificate, or AD changes. Confirm local administrative access independent of SSSD. For a manually created VM, see [the sudo bootstrap runbook](bootstrap_ansible_sudo.md).

Useful tools are provided by `sssd-tools`, `dnsutils`, `netcat-openbsd`, `openssl`, `krb5-user`, and `adcli`. Check what is installed before using a command. Missing tools are not evidence of a backend failure; install approved packages only when repository access works, and do not install or enable a second time/network service as a diagnostic shortcut.

```bash
cat /etc/os-release
sssd --version
sudo systemctl status sssd --no-pager
sudo sssctl config-check
sudo sssctl domain-list
realm list
hostname -f
sudo journalctl -u sssd -b --no-pager -n 100
```

If configuration validation fails, correct that before treating the problem as an offline backend. Inspect `/etc/sssd/conf.d/` as well as `/etc/sssd/sssd.conf`: included snippets can override the main file. SSSD configuration files must be owned by root with mode `0600`.

Set these non-secret values to the exact affected domain, a DC returned by discovery, and an approved test identity. The values below are examples; replace the DC and username before use. `DOMAIN` must match the SSSD domain name; confirm the Kerberos realm separately with the domain administrator.

```bash
export DOMAIN='refol.us'
export REALM='REFOL.US'
export DC='dc.example.com'
export AD_USER='testuser@refol.us'
sudo sssctl domain-status "$DOMAIN"
```

Record online status and the active/discovered servers. Test each affected domain independently. Capture the original configuration before editing:

```bash
SSSD_BACKUP="$(sudo mktemp -d /root/sssd-backup.XXXXXX)"
sudo cp -a /etc/sssd "$SSSD_BACKUP/"
printf 'Configuration backup: %s\n' "$SSSD_BACKUP"
```

Record this path securely. Back up any other file before changing it, including systemd drop-ins and CA trust configuration.

## 2. Capture Backend Evidence

Edit the existing affected domain section rather than adding a second section with the same name:

```bash
sudoedit /etc/sssd/sssd.conf
```

For example, within the existing `[domain/refol.us]` section, temporarily set:

```ini
debug_level = 5
```

Setting this only under `[sssd]` logs the monitor, not the domain backend. Add it to `[pam]` or `[nss]` only when investigating those responders. Level 5 is a starting point; increase only when needed and monitor log growth. Debug output may contain sensitive identity and infrastructure details.

```bash
sudo sssctl config-check
sudo systemctl restart sssd
sudo ls -l /var/log/sssd
sudo tail -F "/var/log/sssd/sssd_${DOMAIN}.log"
```

Use the actual log filename shown by the directory listing; some deployments send logs to the journal. In a separate terminal, trigger a lookup with `id "$AD_USER"` or an approved login attempt and correlate timestamps. Stop following logs with Ctrl+C. A cached result alone does not demonstrate a successful backend exchange.

## 3. Isolate the Failing Layer

| Layer                      | Possible Evidence                                                       | Validation                                                                      | Corrective Direction                                                                                            |
| -------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Network and DNS            | Failed discovery, resolver timeouts, `Resource temporarily unavailable` | Interface/routes, neighbor discovery, DNS SRV records, DC A/AAAA records        | Repair VLAN/bridge/routing or the authoritative resolver path before changing SSSD.                             |
| Transport                  | `PORT_NOT_WORKING`, connection refused/timeouts                         | Bounded connections to the selected DC's required services                      | Review guest, hypervisor, router, and DC firewall rules; an open TCP port alone does not prove protocol health. |
| TLS, when configured       | `Could not start TLS encryption`, issuer/hostname/expiry errors         | Validate the actual LDAPS or StartTLS endpoint                                  | Correct server certificates, hostname, clock, and trusted CA chain without disabling validation.                |
| Kerberos and machine trust | SASL bind failures, clock skew, preauthentication errors                | Time synchronization, keytab principals, `adcli testjoin`, isolated keytab test | Correct DNS/time first; repair machine trust only with evidence and approval.                                   |
| Identity/access policy     | Domain online but lookup or login denied                                | NSS lookup, PAM account checks, actual login and correlated logs                | Review naming, filters, AD/GPO access policy, NSS, and PAM; do not broaden access to hide a failure.            |

### 3.1 Network and DNS

```bash
ip -br addr
ip route
ip neigh show
resolvectl status
readlink -f /etc/resolv.conf
dig +time=2 +tries=1 SRV "_ldap._tcp.dc._msdcs.${DOMAIN}"
dig +time=2 +tries=1 SRV "_kerberos._tcp.${DOMAIN}"
dig +time=2 +tries=1 A "$DC"
dig +time=2 +tries=1 AAAA "$DC"
getent ahosts "$DC"
```

Use `resolvectl` only when systemd-resolved is in use. The LDAP query above is AD-specific; generic LDAP deployments commonly use `_ldap._tcp.<domain>`. Confirm that discovery returns the expected DCs and their addresses are reachable from the VM. Query the approved AD-aware DNS server explicitly with `dig @<dns-server-ip> ...` if the system resolver's answer differs from the intended DNS path.

If `ping` is unavailable or ICMP is blocked, use the transport checks below to generate traffic, then inspect `ip neigh` for an on-link gateway/DC. `FAILED` means neighbor discovery did not succeed; no entry merely means none is currently cached. Fix VLAN/bridge/link configuration before troubleshooting LDAP when the gateway itself cannot be reached.

Persist DNS corrections through the active Netplan, NetworkManager, or systemd-resolved configuration. Do not blindly replace `/etc/resolv.conf`, which may be managed or symlinked. `/etc/hosts` does not supply SRV records and is not a replacement for AD DNS discovery.

### 3.2 Transport and Firewalls

Test the DC actually selected by SSSD, not an arbitrary reachable controller:

```bash
nc -vz -w 3 "$DC" 389
nc -vz -w 3 "$DC" 88
```

If `nc` is unavailable, Bash provides a bounded TCP-only check:

```bash
timeout 3 bash -c 'exec 3<>/dev/tcp/"$1"/389' bash "$DC"
```

Review DNS TCP/UDP 53, Kerberos TCP/UDP 88, LDAP TCP 389, AD discovery/CLDAP UDP 389, and password-change TCP/UDP 464 as required by the deployment. Global Catalog TCP 3268, LDAPS TCP 636, and secure Global Catalog TCP 3269 apply when used. Check the provider's actual requirements rather than assuming every port must be open. A TCP test does not validate UDP discovery, authentication, or TLS.

If UFW manages the guest firewall, inspect `sudo ufw status verbose`. Also review the actual nftables/other policy in use and upstream ACLs. Do not disable firewalls wholesale. Repeat checks against the expected alternate DCs to detect discovery/failover paths blocked by policy.

### 3.3 TLS and Certificate Trust

First establish whether the configured provider uses LDAPS, LDAP StartTLS, or Kerberos SASL protection. The AD provider commonly uses Kerberos-protected LDAP on 389; a closed 636 port alone is not proof of failure.

For configured LDAPS:

```bash
timeout 10 openssl s_client -connect "${DC}:636" -servername "$DC" \
  -verify_hostname "$DC" -verify_return_error \
  -CAfile /etc/ssl/certs/ca-certificates.crt -showcerts </dev/null
```

For configured StartTLS instead:

```bash
timeout 10 openssl s_client -starttls ldap -connect "${DC}:389" -servername "$DC" \
  -verify_hostname "$DC" -verify_return_error \
  -CAfile /etc/ssl/certs/ca-certificates.crt -showcerts </dev/null
```

Require a valid hostname, validity period, and trusted chain. Obtain approved CA certificates from the PKI administrator and verify their fingerprints independently; do not trust a certificate merely because the failing endpoint presented it. Install approved PEM CA certificates, one per `.crt` file, under `/usr/local/share/ca-certificates/`, then run `sudo update-ca-certificates`. Ensure the effective SSSD/OpenLDAP CA settings use the intended trust store, then validate and restart SSSD.

Do not set `ldap_tls_reqcert = never` or weaken signing/encryption as a routine diagnostic or remediation. These changes bypass server verification rather than fixing certificate trust.

### 3.4 Kerberos, Time, and Machine Trust

```bash
date -u
timedatectl status
sudo klist -kte /etc/krb5.keytab
sudo adcli testjoin --domain="$DOMAIN"
```

For hosts using chrony, also run `chronyc tracking` and `chronyc sources -v`. For systemd-timesyncd, use `timedatectl timesync-status`. Correct the existing time service's source/reachability; do not make an unreviewed large clock jump on a production host.

If a direct keytab authentication test is needed, select an exact machine principal from `klist` output, including its realm. Do not assume it is simply the short hostname followed by `$`. Set the example below to the actual principal. Use a separate root-private credential cache so the test cannot overwrite an administrator's existing tickets:

```bash
export MACHINE_PRINCIPAL='ANSIBLE-1$@REFOL.US'
KRB5_TEST_DIR="$(sudo mktemp -d /run/sssd-krb5-test.XXXXXX)"
sudo kinit -c "FILE:${KRB5_TEST_DIR}/ccache" -k -t /etc/krb5.keytab "$MACHINE_PRINCIPAL"
sudo klist -c "FILE:${KRB5_TEST_DIR}/ccache"
```

If authentication succeeded, destroy only that test cache, then remove the empty test directory:

```bash
sudo kdestroy -c "FILE:${KRB5_TEST_DIR}/ccache"
sudo rmdir "$KRB5_TEST_DIR"
```

If authentication failed, preserve the error and inspect/clean only the test directory; do not run a broad `kdestroy -A`. Keytab files do not simply expire like tickets: machine-password mismatch, account reset, wrong principal, unsupported encryption, DNS, or clock errors require different remedies. A successful keytab test proves that principal's Kerberos authentication, not every SSSD/PAM path.

Do not leave/rejoin the domain as the first response. For confirmed broken trust, coordinate computer-account repair with the AD administrator, back up configuration and keytab securely, and use an approved trust-repair/rejoin procedure in a maintenance window. A keytab backup alone does not restore an AD machine password changed server-side.

## 4. Apply Evidence-Based Remediation

Make one change at a time, validate the configuration, and repeat the failing check. Prefer correcting the network, resolver, certificate, or trust problem over tuning timeouts or clearing state.

### 4.1 Boot-Time Ordering

Use this only when boot timestamps show SSSD starting before the required network is configured and it works after connectivity recovers. Inspect existing dependencies first:

```bash
sudo systemctl cat sssd
systemd-analyze critical-chain sssd.service
sudo journalctl -b -u sssd -u systemd-networkd -u systemd-resolved --no-pager
```

For NetworkManager guests, inspect its journal instead. Ensure the appropriate wait-online service for the actual network renderer is enabled and correctly configured; do not enable both renderers' wait services blindly. If an ordering change is justified, use `sudo systemctl edit sssd.service` and add:

```ini
[Unit]
Wants=network-online.target
After=network-online.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart sssd
sudo systemctl status sssd --no-pager
```

`network-online.target` is a boot-time synchronization point, not proof that DNS or a DC is reachable and not an ongoing connectivity monitor. This is not a guaranteed cure for offline states. Review for dependency cycles and verify at the next approved reboot; do not reboot solely to mask unresolved networking.

### 4.2 Restrict Address Lookups Only When Justified

An AAAA response with no data is normal for an IPv4-only host and does not by itself explain an LDAP connection failure. Investigate incorrect A/AAAA records and unreachable advertised addresses first.

If evidence and network policy justify restricting this SSSD domain to IPv4, add this to its existing `[domain/...]` section:

```ini
lookup_family_order = ipv4_only
```

The option is `lookup_family_order`, not `lookup_family`. Run `sudo sssctl config-check`, restart SSSD in the approved window, and repeat discovery and login checks. Remove the restriction if it does not address the demonstrated failure or IPv6 is required.

### 4.3 Refresh Cached State Last

Do not clear caches while the backend is unreachable: cached credentials may be the only available domain login path. First repair connectivity and trust. For a stale test identity, prefer a targeted expiration:

```bash
sudo sss_cache -u "$AD_USER"
id "$AD_USER"
```

Expiration marks an entry stale; it does not erase the whole database or prove a fresh online fetch succeeded. Correlate with online status and logs.

Use `sudo sssctl cache-remove` only as an approved last resort after checking its installed version's `--help`, securing local recovery access, and backing up required local overrides with `sudo sssctl local-data-backup`. Follow interactive stop/start prompts and confirm SSSD is running afterward. Removing caches discards cached identities/credentials and can prevent offline logins until users authenticate online again; a local-data backup is not a backup of all cached credentials.

Do not follow a failed cache-remove operation with wildcard deletion of `/var/lib/sss/db/*` or `/var/lib/sss/mc/*`. Preserve the error and escalate for a version-specific recovery procedure rather than destroying evidence and authentication state.

## 5. Verify Operational Recovery

```bash
sudo sssctl config-check
sudo systemctl is-active sssd
sudo sssctl domain-status "$DOMAIN"
id "$AD_USER"
getent passwd "$AD_USER"
sudo sssctl user-checks -a acct -s sshd "$AD_USER"
```

| Check                    | Acceptance Criteria                                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Configuration and daemon | Configuration validation succeeds; service is `active`.                                                                                                                                                                      |
| Backend connectivity     | Affected domain reports online with the expected active server; new requests do not immediately return it to offline.                                                                                                        |
| Identity                 | `id` and `getent` return the expected UID, GID, and groups. Results may be cached and are not authentication tests.                                                                                                          |
| Account authorization    | PAM account checks permit the intended service/user; failures are reviewed against actual AD/GPO and local policy. This is not a password test.                                                                              |
| Authentication/session   | A fresh approved domain login through the intended PAM service succeeds with the required authentication method. Correlated logs establish online authentication rather than only cached login or an unrelated SSH-key path. |
| Persistence              | Recovery survives normal retry/failover and the next approved reboot when boot ordering was implicated.                                                                                                                      |

`kinit` with an approved user principal can separately validate Kerberos password authentication, but it does not exercise the complete SSH/PAM/SSSD login path. Avoid repeated failed password tests that could lock the account. Keep the local recovery session open until a separate domain session is verified.

## 6. Restore Normal Settings and Record the Fix

Remove temporary debug settings or restore their prior values, validate the configuration, and restart SSSD if configuration changed. Retest online status and a fresh login after restoring normal logging. Remove test credential caches and retain sensitive diagnostic artifacts only under the approved access and retention policy.

If a change failed, restore only the affected configuration from the recorded backup, maintaining root ownership and mode `0600` for SSSD configuration. For systemd overrides, restore the prior file or remove only the lines/drop-in created for this incident; do not use a blanket revert that discards unrelated customizations. Run `systemctl daemon-reload` after unit changes, validate SSSD configuration, and restart in the approved window. Cache deletion and AD computer-account changes require their own recovery plan; restoring a config file does not reverse them.

Record the root cause, evidence, changes, tests, and remaining risks. Persist approved configuration changes in the owning automation so later runs do not undo them. The repository's [AD role](../../roles/ad/tasks/main.yml) changes DNS and SSSD settings and restarts/reboots the guest. Its [join playbook](../../playbooks/ad/join_domain.yml) is provisioning automation, not a general offline-backend repair: it discovers membership and joins only when discovery reports it unconfigured. Do not run it blindly or assume it repairs a stale machine keytab on an already configured host.

## References

These commands/options were checked against Ubuntu 24.04's SSSD 2.9 documentation and systemd documentation. Consult the affected host's installed manuals and `sssctl COMMAND --help` for release-specific behavior.

- [SSSD configuration, logging scope, and address-family order](https://manpages.ubuntu.com/manpages/noble/en/man5/sssd.conf.5.html)
- [LDAP transport, certificate verification, and keytab settings](https://manpages.ubuntu.com/manpages/noble/en/man5/sssd-ldap.5.html)
- [SSSD control utility](https://manpages.ubuntu.com/manpages/noble/en/man8/sssctl.8.html)
- [systemd network-online target semantics](https://www.freedesktop.org/software/systemd/man/latest/systemd.special.html#network-online.target)
