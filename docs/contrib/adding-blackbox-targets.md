# 🌐 Runbook: Adding Blackbox Exporter Targets

## 📖 Purpose

This runbook explains how to add, update, or remove web probe targets for the Prometheus Blackbox Exporter in this repository.

The single source of truth for blackbox targets is:

```yaml
inventory/prometheus/group_vars/all/main.yml
```

Do not edit rendered Prometheus configuration on the host. Do not rely on previously deployed scrape targets remaining in place. The inventory list is authoritative.

---

## 🧭 How Blackbox Targets Work Here

Blackbox targets are defined in `prometheus_setup_blackbox_targets` and are rendered into the Prometheus scrape configuration by the `prometheus_setup` role.

Each target supports:

| Field        | Required | Purpose                                                                   |
| ------------ | -------- | ------------------------------------------------------------------------- |
| `target`   | Yes      | The URL Prometheus should probe through Blackbox Exporter                 |
| `instance` | Yes      | The friendly service name shown in Grafana                                |
| `group`    | No       | A logical grouping label; defaults to the configured blackbox group label |

Example:

```yaml
prometheus_setup_blackbox_targets:
  - target: "http://192.168.20.155:3579"
    instance: "ombi.refol.us"
    group: "web"
```

---

## 🛠 Add a New Target

### 1. Edit the Prometheus inventory group vars

Open:

```yaml
inventory/prometheus/group_vars/all/main.yml
```

Add a new item under `prometheus_setup_blackbox_targets`:

```yaml
  - target: "http://192.168.20.200:8080"
    instance: "example.refol.us"
    group: "web"
```

Guidelines:

* Use the real URL or IP:port that should answer the probe.
* Use `instance` as the stable, human-friendly service name.
* Keep `group: "web"` unless you have a clear reason to segment dashboards or queries differently.
* Do not add leading or trailing whitespace to `target` values.
* Prefer one entry per externally meaningful service endpoint.

---

## ✏️ Update an Existing Target

If a service moves or changes ports:

1. Find the existing item in `prometheus_setup_blackbox_targets`
2. Update the `target`
3. Keep `instance` the same if the service identity has not changed

Example:

```yaml
  - target: "http://192.168.20.210:8080"
    instance: "example.refol.us"
    group: "web"
```

This preserves Grafana naming and keeps dashboards readable even when the backend address changes.

---

## 🗑 Remove a Target

To stop probing a service, delete its item from `prometheus_setup_blackbox_targets`.

Because inventory is the only source of truth, removing the entry and redeploying Prometheus exporters removes that target from the generated Prometheus configuration.

---

## ✅ Validate the Change

If Ansible is installed in the repo Python environment:

```bash
source /opt/python_3.12/bin/activate
ansible-playbook -i inventory/prometheus/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml --syntax-check
```

This confirms the playbook and the rendered Prometheus configuration path still parse correctly.

---

## 🚀 Deploy the Updated Target List

Run:

```bash
ansible-playbook -i inventory/prometheus/inventory.ini playbooks/prometheus/deploy_prometheus_exporters.yml
```

If you normally use a shell variable for the inventory, use your existing repo workflow instead.

This updates the Prometheus configuration so the new blackbox target list is applied.

---

## 🔍 Verify After Deployment

### In Prometheus

Check the blackbox job in the Prometheus UI and confirm the new target appears.

Useful queries:

```promql
probe_success{job="blackbox_http"}
```

```promql
probe_duration_seconds{job="blackbox_http"}
```

Expected behavior:

* `instance` should be the friendly name from inventory, such as `ombi.refol.us`
* `target` should contain the probed URL
* `probe_success` should be `1` for healthy services and `0` for failing services

### In Grafana

Open the Web Service Status dashboard and confirm:

* the service appears by `instance` name, not raw URL
* status tiles reflect `probe_success`
* latency panels reflect `probe_duration_seconds`

---

## ⚠️ Common Mistakes

* Editing the generated Prometheus config instead of inventory
* Leaving a stale target in inventory after a service migration
* Changing `instance` when only the backend URL changed
* Introducing whitespace into the `target` value
* Using an unreachable backend URL while expecting the reverse proxy hostname to be probed

---

## ✅ Summary

To manage blackbox targets:

1. Edit `prometheus_setup_blackbox_targets` in `inventory/prometheus/group_vars/all/main.yml`
2. Run the Prometheus exporter syntax check
3. Deploy `playbooks/prometheus/deploy_prometheus_exporters.yml`
4. Verify the target in Prometheus and Grafana

The inventory list is authoritative, and redeploying applies the exact target set defined there.
