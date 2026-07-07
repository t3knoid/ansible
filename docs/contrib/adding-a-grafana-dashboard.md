# 📊 Runbook: Adding a Grafana Dashboard

## 📖 Purpose

This runbook describes how to add a new Grafana dashboard in this repository using the existing dashboard-as-code pattern.

Grafana dashboards in this repo are managed as JSON files in the `grafana_setup` role and deployed through Ansible provisioning.

---

## 🧭 Scope

This runbook applies to:

* Grafana dashboard JSON files managed by Ansible
* Grafana datasource and dashboard provisioning managed by the `grafana_setup` role

---

## 🛠 Add a New Dashboard

### 1. Add the dashboard JSON file to the Grafana role

Place the dashboard JSON file under:

```text
roles/grafana_setup/files/dashboards
```

Example:

```bash
cp /path/to/your-dashboard.json roles/grafana_setup/files/dashboards/my-dashboard.json
```

Guidelines:

* Prefer an upstream dashboard JSON as a base when one exists.
* Keep the dashboard UID stable so Grafana updates the existing dashboard instead of creating duplicates.
* Use a clear filename that matches the dashboard purpose.

---

### 2. Add Grafana role defaults only when needed

If the dashboard requires new settings, add them in:

```text
roles/grafana_setup/defaults/main/main.yml
```

Typical examples:

* datasource name or UID
* folder or dashboard path settings
* dashboard provider refresh interval

Only add variables that are required for the dashboard you are introducing.

---

### 3. Ensure provisioning and copy tasks include the dashboard

Confirm the Grafana role includes the expected provisioning and copy logic in:

```text
roles/grafana_setup/tasks/main.yml
```

Check that these are present and aligned:

* datasource provisioning template task
* dashboard provider provisioning template task
* copy task for the dashboard JSON into the Grafana dashboards path

Also confirm the provisioning templates are correct:

```text
roles/grafana_setup/templates/provisioning-datasources.yml.j2
roles/grafana_setup/templates/provisioning-dashboards.yml.j2
```

For a new dashboard file, add a matching copy task in `roles/grafana_setup/tasks/main.yml` so the JSON is installed into Grafana's dashboards directory.

---

### 4. Deploy Grafana

Deploy the updated Grafana role with:

```bash
ansible-playbook -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana.yml
```

This applies the new dashboard JSON and any related provisioning changes to the Grafana hosts.

---

## ✅ Validate

Before or after deployment, run:

```bash
source /opt/python_3.12/bin/activate
ansible-playbook --syntax-check -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana.yml
ansible-inventory -i inventory/grafana/inventory.ini --graph
python3 -m json.tool roles/grafana_setup/files/dashboards/my-dashboard.json >/dev/null
```

These checks confirm:

* the Grafana deployment playbook parses correctly
* the Grafana inventory resolves correctly
* the dashboard JSON is valid

---

## 🔍 Verify After Deployment

In the Grafana UI, confirm:

* the dashboard appears in the expected folder
* the panels load data successfully
* the Prometheus datasource resolves correctly

If the dashboard is intended to be a landing page or linked dashboard, also confirm the navigation path works as expected.

---

## ⚠️ Troubleshooting

### Dashboard not visible

Check the following:

* the JSON file exists under `roles/grafana_setup/files/dashboards`
* the copy task in `roles/grafana_setup/tasks/main.yml` uses the same filename
* the dashboard provider provisioning still points at the correct dashboards directory
* Grafana restarted or reloaded after the provisioning change

### Panels show datasource errors

Check the following:

* datasource provisioning template values are correct
* the Prometheus URL or host resolution is correct for the active inventory
* the dashboard JSON references the expected datasource UID

### Dashboard duplicates appear

Check the following:

* the dashboard UID has not changed unintentionally
* the dashboard filename and copy task still refer to the same dashboard artifact

---

## ✅ Summary

To add a new Grafana dashboard:

1. Add the JSON file under `roles/grafana_setup/files/dashboards`
2. Add any required defaults in `roles/grafana_setup/defaults/main/main.yml`
3. Ensure `roles/grafana_setup/tasks/main.yml` copies and provisions the dashboard
4. Deploy [playbooks/grafana/deploy_grafana.yml](playbooks/grafana/deploy_grafana.yml)
5. Validate the JSON, deployment path, and dashboard behavior in Grafana

The existing `grafana_setup` role is the source of truth for how dashboards are provisioned and deployed in this repository.
