# Observability Traffic Dashboard

The Observability Landing dashboard summarizes node, Proxmox VE, web-service,
and main reverse-proxy health. Its traffic views cover `rproxy-0`, with total
request rate, selected-window request count, the most requested domain, top
domains, HTTP response classes, and a request-duration histogram.

## Deployment

Deploy the collector, refresh Prometheus targets, then update Grafana:

```bash
ansible-playbook -i inventory/rproxy/inventory.ini -k playbooks/prometheus/deploy_nginxlog_exporter.yml -u ansible
ansible-playbook  -i inventory/rproxy/inventory.ini -k playbooks/prometheus/deploy_prometheus_exporters.yml -u ansible
ansible-playbook -i inventory/grafana/inventory.ini -k playbooks/grafana/deploy_grafana.yml
```

The scrape refresh deliberately uses the default combined inventory. Do not scope it to the Grafana inventory or limit it to `rproxy-0`: it runs on
`prometheus-0` and preserves previously registered exporter targets.

Open Grafana's existing home dashboard or `/d/observability-landing`. Allow a few scrape intervals for rate and increase queries to have sufficient samples.
Domain rankings and latency history begin after collector deployment; earlier traffic is not reconstructed. Empty domain panels before collection are expected.

## Collection

`nginxlog_exporter_setup` runs the pinned `prometheus-nginxlog-exporter` release as an unprivileged systemd service on the main proxy's private IP, port `4040`. Prometheus scrapes it every 15 seconds under the `nginxlog_exporter` job.

Nginx writes a dedicated `/data/nginx/log/traffic.log`, rotated daily with seven retained files. This log stores configured server name, request method, protocol,
status, response bytes, and duration. It does not store client IPs, request paths, query strings, cookies, or authorization headers. The domain label comes from
`$server_name`, not untrusted incoming Host headers.

The logging directive is inherited from nginx's HTTP context. A custom server or location with its own `access_log` directive overrides that inheritance; add
the `rproxy_metrics` log there too if such a site must be included.

Total traffic uses nginx's existing global request counter. Domain rankings and duration buckets count completed requests from the dedicated log, so totals can
differ, particularly for long-lived streams. Both include monitoring requests. The rankings use the dashboard's selected time range. Prometheus `increase`
estimates counts between scrapes, rather than providing billing-grade totals.

## Verification

On `rproxy-0`, check `systemctl status nginxlog-exporter` and
`nginx -t`. The metric endpoint is `http://<rproxy-0-private-ip>:4040/metrics`.
After visiting a site, look for `nginxlog_http_response_count_total` with a
`domain` label and `nginxlog_http_response_time_seconds_hist_bucket` with a
`le` label. `nginxlog_parse_errors_total` should not increase during normal use.

In Prometheus, check `up{job="nginxlog_exporter",instance="rproxy-0"}`.
The dashboard's Traffic Collector status should show Up after deployment.