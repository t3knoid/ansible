# Decommission a VM

Use this procedure to retire a Proxmox VM, remove its DNS records and monitoring
targets, and clean up the repository. Run controller commands from the repository
root with the usual vault credentials available. Examples use `retired-0`;
replace it with the exact inventory hostname. These commands are operational
instructions, not a dry run.

If the VM has already been deleted, verify its absence in Proxmox, skip the
shutdown/removal commands, and use the DNS-only recovery path in section 3 before
continuing with monitoring and repository cleanup. Do not recreate a VM just to
run this procedure.

## 1. Prepare and approve

- Record the hostname, FQDN, IP address, Proxmox node and VMID, service aliases,
  application owner, dependencies, and approved retirement date.
- Confirm that traffic, scheduled jobs, integrations, and data have moved to the
  replacement service. Check databases, shared storage, reverse proxies, and
  other consumers before shutting down the VM.
- Take or verify a restorable backup and agree its retention period. A snapshot
  on the VM being deleted is not an independent backup. Export required data,
  configuration, and audit records before deletion.
- Preserve the host's inventory, host variables, global IP mapping, and any
  Terraform configuration/state until VM and DNS removal have succeeded.
- Check the effective `vms_use_terraform` setting. Terraform-managed VMs must use
  their existing configuration and state; do not switch to the Ansible removal
  path to bypass an ownership or state error.
- Arrange a maintenance window and, if necessary, a temporary Alertmanager or
  Grafana silence. A silence suppresses notifications; it does not remove targets.
- Retire one VM at a time. Never run an unscoped removal command.

Identify the VM and preview the selected hosts:

```bash
ansible-playbook playbooks/vms/show_vm_id.yml --limit retired-0
ansible-playbook playbooks/vms/show_vm_node.yml --limit retired-0
ansible-playbook playbooks/vms/remove_vm.yml --limit retired-0 --list-hosts
```

The removal play targets the `removable` group. Ensure the existing host is a
member of that group, following the local inventory pattern, then repeat
`--list-hosts`. It must list only the intended VM. An empty selection is not
successful removal. The full combined inventory is the default in this repo;
keep it available so delegated infrastructure hosts and variables resolve.

## 2. Remove service aliases and drain traffic

Remove or redirect reverse-proxy routes and client integrations first. If an
alias now belongs to a replacement service, update it instead of deleting it.

For aliases that really are being retired, review the host's
`pihole_cname_entries` and preview the existing CNAME removal play:

```bash
ansible-playbook playbooks/dns/delete_cname_entry.yml --limit retired-0 --list-hosts
ansible-playbook playbooks/dns/delete_cname_entry.yml --limit retired-0
```

This play targets `cname` and deletes the configured entries for the selected
host. Confirm membership and the complete entry list before running it. An alias
may point to a shared reverse proxy rather than directly to the retired VM;
inspect the service's records, not just aliases whose target is the VM's FQDN.
Check external DNS, other DNS zones, AAAA/PTR records, and DHCP reservations
separately where applicable. Do not delete shared service records.

Remove retired aliases from their repository definitions after the API operation
succeeds so a later DNS deployment cannot recreate them.

## 3. Remove the VM from Proxmox and its host DNS record

Optionally shut down gracefully and verify that no required service is lost:

```bash
ansible-playbook playbooks/vms/shutdown_vm.yml --limit retired-0
```

Perform the approved removal:

```bash
ansible-playbook playbooks/vms/remove_vm.yml --limit retired-0
```

Inspect the displayed VM list and enter `yes` only when it is correct.
The [removal playbook](../../playbooks/vms/remove_vm.yml):

1. Acquires the VM workflow lock.
2. Stops and removes an Ansible-managed VM, or validates Terraform ownership and
   applies a confirmed destroy-only plan for a Terraform-managed VM.
3. Clears the host's finalization checkpoint.
4. Deletes the Pi-hole host record only after the VM removal tasks succeed.
5. Releases the workflow lock even if a task fails.

VM removal is destructive. It is not a backup-retention or secure-erasure policy;
verify attached disks, unused volumes, storage snapshots, replication/HA entries,
and backup schedules in Proxmox rather than assuming every artifact was removed.

Confirm the VMID is absent in Proxmox. Confirm the exact Pi-hole host record
`<IP> <hostname>.<global_domain_name>` is absent, and verify DNS propagation on
every serving resolver, including any secondary synchronized Pi-hole. Allow for
client caches and TTLs; inspect authoritative configuration as well as queries.

If the VM was already deleted, or VM removal succeeded but DNS cleanup failed,
keep the inventory/IP mapping and use the DNS-only playbook:

```bash
ansible-playbook playbooks/dns/delete_dns_entry.yml --limit retired-0 --list-hosts
ansible-playbook playbooks/dns/delete_dns_entry.yml --limit retired-0
```

It targets `vms`, `synology`, and `pvenodes` and removes the configured Pi-hole
host record, not CNAMEs. Do not rerun destructive VM removal solely to retry DNS.
Resolve Terraform state/ownership failures explicitly; do not delete state files
or force removal to make the error disappear.

## 4. Remove Prometheus scrape and probe targets

The [exporter refresh tasks](../../roles/prometheus_setup/tasks/exporters.yml)
read the live Prometheus configuration and merge inventory targets into it.
**Removing inventory entries and running a refresh does not prune old targets.**
Use the [target-removal playbook](../../playbooks/prometheus/remove_prometheus_targets.yml)
after removing their repository definitions.

1. Remove the retired host from exporter groups in the repository. Review `node_exporter`,
   `nginx_exporter`, `nginxlog_exporter`, `postgres_exporter`, `pve_exporter`, and
   `ceph_nodes` as applicable. Search by hostname, IP, and service aliases.
2. Remove retired HTTP probes from `prometheus_setup_blackbox_targets`, including
   those in [the Prometheus inventory variables](../../inventory/prometheus/group_vars/all/main.yml).
   Probe instance labels can be service FQDNs rather than VM hostnames. Preserve
   probes that now monitor a replacement service.
3. Preview exact instance-label removals from the controller:

   ```bash
   ansible-playbook playbooks/prometheus/remove_prometheus_targets.yml --check -e '{"prometheus_setup_remove_instances":["retired-0","retired.example.test"]}'
   ```

Include only retired labels; service probe labels can differ from VM names.
This preview reads the live configuration and reports whether it would change,
but does not write, run `promtool`, or reload Prometheus. 4. Apply the same selection without `--check`:

```bash
ansible-playbook playbooks/prometheus/remove_prometheus_targets.yml -e '{"prometheus_setup_remove_instances":["retired-0","retired.example.test"]}'
```

The playbook runs on the `prometheus` group, not the retired VM. It parses YAML
structurally and changes only selected jobs' `static_configs`. An exact
`labels.instance` match removes that whole static entry, including all targets
sharing its labels. Review shared labels before selecting them. To remove only
a particular endpoint from a shared entry, use literal target selection:

```bash
ansible-playbook playbooks/prometheus/remove_prometheus_targets.yml -e '{"prometheus_setup_remove_targets":["192.0.2.10:9200","https://retired.example.test"]}'
```

Replace the documentation IP/URL above. Both selection lists can be combined;
matching either selects removal. No wildcards, substring matches, or automatic
IP/hostname expansion are used. Empty static entries are dropped; unrelated
jobs, targets, service discovery, labels, and shared exporter endpoints remain. 5. The task stages a private candidate next to the live config and runs
`/opt/prometheus/promtool check config` against it. Only after successful
validation does it back up and atomically replace the live file, preserving
its owner and permissions, then POST locally to `http://localhost:9090/-/reload`.
Validation failure leaves the original untouched. Reload failure restores the
backup, attempts a reload of the restored config, and fails the play for review.
A repeated run with no matching targets does not rewrite or reload anything.

Defaults are `/data/prometheus/etc/prometheus.yml` and the jobs `node`,
`nginx_exporter`, `nginxlog_exporter`, `postgres_exporter`, `pve_exporter`, `ceph`,
and `blackbox_http`. Override `prometheus_setup_config_file`,
`prometheus_setup_home`, `prometheus_setup_remove_reload_url`, or
`prometheus_setup_remove_jobs` for a custom deployment. PostgreSQL, PVE, Ceph,
and Blackbox job defaults follow their existing role job-name variables.
YAML comments/formatting may change; the original file is retained in a
timestamped Ansible backup beside it. Serialize this operation with other
Prometheus configuration deployments. 6. Confirm the targets no longer appear in Prometheus Target Health and that
`prometheus_config_last_reload_successful` is `1`. A removed target should not
remain listed as `DOWN`. Check that unrelated targets are still healthy.

After repository target definitions and the live configuration are cleaned up,
the normal refresh can be run from the controller:

```bash
ansible-playbook playbooks/prometheus/deploy_prometheus_exporters.yml
```

Use the full default combined inventory, not a single service inventory or a
`--limit` for the retired VM: this play runs on the Prometheus host. Verify that
retired targets remain absent after the refresh. Do not use
`deploy_prometheus.yml` as a pruning command; it is the broader installation play.

Review any host-specific Prometheus alert rules, recording rules, and external
checks. Remove obsolete `absent()` checks that would otherwise keep alerting after
target removal. If the VM was represented by metrics from a shared Proxmox or
database exporter, keep that shared exporter and verify the retired resource is
no longer reported. Historical series remain until retention expires; do not
delete the Prometheus data directory or invoke destructive series deletion just
to retire a host.

## 5. Remove Grafana references

Grafana normally queries Prometheus; there is no separate host-registration
record to delete. The [Node Exporter dashboard](../../roles/grafana_setup/files/dashboards/node-exporter-overview.dashboard.json)
uses `label_values(node_uname_info, instance)` for its host selector.

- Reload dashboards and check current-time panels after Prometheus cleanup.
  Historical queries and host dropdowns may still show the VM while its series
  remain in the requested time range or retained label metadata.
- Remove or update dedicated host dashboards, fixed panel queries, annotations,
  variable defaults, and Grafana-managed alert rules referencing the retired host.
  Verify that remaining rules do not enter an unexpected No Data/Error state.
- If a provisioned dashboard needs changing, update its repository source rather
  than only editing the UI. Use the existing [Grafana deployment playbook](../../playbooks/grafana/deploy_grafana.yml)
  after reviewing its scope: it also runs Azure CLI and Entra ID application
  setup, not just dashboard provisioning.

  ```bash
  ansible-playbook -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana.yml
  ```

- Do not redeploy Grafana merely to clear a host dropdown. Do not delete a shared
  Prometheus data source, shared dashboard, or notification contact point.
- Remove temporary silences when cleanup is verified; preserve useful historical
  dashboards/data according to the agreed retention policy.

## 6. Finish repository and infrastructure cleanup

Only after VM and DNS operations succeed:

- Remove the hostname from all inventories/groups, including `removable`, and
  remove obsolete `host_vars`. Keep unrelated hosts in shared inventory files.
- Remove its entry from `global_ip_addresses` in
  [the global variables](../../roles/global/vars/main.yml). Release/reuse the address
  only after DNS caches, DHCP reservations, and other consumers are addressed.
- Remove obsolete reverse-proxy, OAuth application/callback, certificate-renewal,
  firewall/NAT, VPN, load-balancer, and service-discovery definitions. Apply changes
  through the relevant existing service playbooks after reviewing their scope.
- Remove retired backup jobs, scheduled tasks, CI/deployment targets, and external
  uptime checks. Keep retained backups and their restore credentials until expiry.
- Revoke host-specific credentials, SSH keys, API tokens, and machine accounts as
  applicable. Do not revoke shared credentials still used by other services.
- Remove obsolete SSH known-host entries for the hostname, FQDN, and IP on relevant
  controllers/clients. Review controller caches and generated cloud-init artifacts
  for sensitive data. Preserve Terraform state/history for audit and recovery;
  archive it securely rather than deleting it as routine cleanup.
- Record the deletion result, retained backups, state archive location, released
  IP/VMID, outstanding cleanup, and owner approval in the change record.

Use `rg` to check for stale references, reviewing each match rather than blindly
deleting shared configuration:

```bash
rg -n -F -e 'retired-0' -e 'RETIRED_IP' -e 'RETIRED_SERVICE_FQDN' inventory roles playbooks terraform
```

Replace all three example values before searching. Validate each affected
inventory with `ansible-inventory -i inventory/<name>/inventory.ini --graph`.
Syntax-check any changed playbooks against the relevant inventory before applying.
Review the diff and commit through the normal review process; do not manually
edit generated inventory, role, or playbook documentation.

## Acceptance and recovery

- Proxmox: VM absent; attached storage and retained backups accounted for.
- DNS: retired host record and obsolete aliases absent on all serving resolvers.
- Prometheus: targets absent, reload successful, no obsolete host-specific alerts,
  and unrelated targets healthy, including after a normal exporter refresh.
- Grafana: live dashboards and alerts no longer depend on the host. Historical
  appearance alone is not evidence that scraping continues.
- Repository: no active definition can recreate the host's records or targets;
  remaining historical references are intentional.

Before deletion, recovery can mean restoring routes/DNS and restarting the VM.
After deletion, recovery requires a verified backup or a controlled rebuild and
data restore; recreating DNS alone does not restore the service. If a step fails,
record completed stages and resume the failed cleanup stage. Do not repeat VM
destruction or restore stale monitoring configuration indiscriminately.

## Streamlined playbook scaffold

The [decommission playbook](../../playbooks/vms/decommission_vm.yml) currently
provides an inventory-only preview. It requires explicit hostnames in both `vms`
and `removable`, with global IP mappings, and rejects execution requests. It does
not query Proxmox, verify backups/ownership, or remove any resources.

```bash
ansible-playbook playbooks/vms/decommission_vm.yml -e '{"decommission_hosts":["retired-0"]}'
```

Use the default combined inventory. The scaffold runs on `localhost`; select VMs
with `decommission_hosts`, not `--limit retired-0`, which would exclude the
controller play. Follow the operational sections above for actual retirement.

The remaining workflow should use reusable tasks rather than a shell wrapper
around several `ansible-playbook` commands. Intended implementation contract:

- Require an explicit list of inventory hostnames and a separate destruction
  confirmation. Reject unknown hosts, broad/wildcard selections, and an empty
  list. Default to a read-only plan that prints VMIDs, ownership, DNS records,
  scrape/probe entries, and impacted services without exposing secrets.
- Keep the existing `global` setup, VM workflow lock, Terraform ownership checks,
  and destroy-plan validation from `remove_vm.yml`. Refactor its guarded removal
  workflow for reuse so confirmation and lock handling cannot be bypassed.
- Validate backups/approval inputs and all required infrastructure access before
  deletion. Process hosts individually and verify VM absence before DNS deletion.
- Add an explicit already-absent cleanup mode that verifies Proxmox absence and
  reconciles Terraform ownership/state without bypassing its safeguards.
- Remove exact reviewed Pi-hole host records and obsolete CNAMEs, then verify
  primary and secondary resolvers. Preserve aliases moved to replacement services.
- Integrate the implemented `prometheus_setup` role's `remove_targets.yml` tasks
  into the orchestrator, running on the Prometheus server rather than the retired
  guest. Supply reviewed exact instance labels/endpoints; never prune every target
  missing from a partial inventory. Live target removal is already available through
  [the standalone playbook](../../playbooks/prometheus/remove_prometheus_targets.yml).
- Make retirement exclusions persistent so an ordinary exporter refresh cannot
  reintroduce selected targets before inventory cleanup. Apply exclusions after
  the existing merge, with tests covering stale inventory and service probe aliases.
- Audit Grafana references and report shared resources needing review. Automate
  deletion only for explicitly selected, exclusively owned resources; leave shared
  dashboards/data sources and historical metric data untouched.
- Produce a per-host completion report and a proposed repository diff for review,
  rather than automatically rewriting inventories, deleting state, or committing.
  Persist stage results so retries resume cleanup without repeating destruction.

Test the proposed workflow with mocked infrastructure before live use, including
wrong-host rejection, failed VM removal preserving DNS, already-absent VMs,
Terraform ownership mismatch, aliases moved to replacements, shared exporter
preservation, failed Prometheus validation leaving the active config intact, and
safe reruns. Do not advertise Ansible `--check` as a safe preview until all
destructive paths have explicit coverage for it.
