# 📊 Service Path Dashboard Generator

## 🔧 Overview
`scripts/generate_service_path_dashboard.py` generates the Grafana **Service Path** dashboard:

```
roles/grafana_setup/files/dashboards/service-path.dashboard.json
```

The dashboard is generated rather than edited by hand because its Canvas panel has dozens of elements and
paired connections that must reference matching field names and value mappings. Change the script, then
regenerate the JSON and commit both files.

For how the dashboard works (probes, recording rules, panels), see
[Service Path Dashboard](../contrib/service-path-dashboard.md).

---

## ▶️ Usage

```bash
python3 scripts/generate_service_path_dashboard.py              # default output path above
python3 scripts/generate_service_path_dashboard.py /tmp/x.json  # write somewhere else
```

The script uses only the Python standard library. Deploy the result with:

```bash
ansible-playbook -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana_dashboards.yml
```

---

## 🧩 What the script contains

| Part | Purpose |
|---|---|
| Value mappings (`NODE_MAP`, `HOP_MAP`, `FLOW_MAP`, `DIAG`) | Health value → text and colour; failure code → text |
| `stat()`, `panel()`, `row()`, `target()` helpers | Build panels and Prometheus queries |
| `node()`, `conn()`, `label()`, `hop_label()` | Build Canvas boxes, hop/flow connection pairs and labels |
| Layout constants (`X_*`, `R_*`) | Column centres and row tops, in percent of the Canvas panel |
| Section blocks | Service overview, Service path, Component health, Probe details, Failure summary |

When adding a recording-rule value (for example a new failure code), update the matching mapping here and
the decision table in the docs.
