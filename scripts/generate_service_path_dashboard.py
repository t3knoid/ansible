#!/usr/bin/env python3
"""
Generates the Service Path Grafana dashboard
(roles/grafana_setup/files/dashboards/service-path.dashboard.json).

The dashboard reads the service_path:* recording rules and the `service_path` Blackbox job
rendered by the prometheus_setup role from `service_path_services`. Edit this script rather
than the JSON, then regenerate and deploy:

    python3 scripts/generate_service_path_dashboard.py
    ansible-playbook -i inventory/grafana/inventory.ini playbooks/grafana/deploy_grafana_dashboards.yml
"""
import json
import os
import sys

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "roles", "grafana_setup",
                              "files", "dashboards", "service-path.dashboard.json")

DS = {"type": "prometheus", "uid": "prometheus"}
J = 'job="service_path"'
SVC = 'service="$service"'

GREEN, YELLOW, RED, GRAY, BLUE = "#73BF69", "#FADE2A", "#F2495C", "#8E8E8E", "#5794F2"
INK = "#111217"

NODE_MAP = [{"type": "value", "options": {
    "2": {"text": "OK", "color": GREEN, "index": 0},
    "1": {"text": "DEGRADED", "color": YELLOW, "index": 1},
    "0": {"text": "FAILED", "color": RED, "index": 2}}}]
HOP_MAP = [{"type": "value", "options": {
    "2": {"text": "ok", "color": "rgba(115,191,105,0.45)", "index": 0},
    "1": {"text": "slow", "color": "rgba(250,222,42,0.7)", "index": 1},
    "0": {"text": "BROKEN", "color": RED, "index": 2}}}]
FLOW_MAP = [{"type": "value", "options": {
    "2": {"text": "flowing", "color": GREEN, "index": 0},
    "1": {"text": "flowing (slow)", "color": YELLOW, "index": 1}}}]

DIAG = {
    0: ("Healthy", GREEN),
    1: ("DNS FAILURE: public and internal resolution failing", RED),
    2: ("EXTERNAL PATH FAILURE: public DNS", RED),
    3: ("INTERNAL PATH FAILURE: internal DNS", RED),
    4: ("EXTERNAL PATH FAILURE: Cloudflare / public edge", RED),
    5: ("INTERNAL PATH FAILURE: LAN cannot reach rproxy-0 (Cloudflare can)", RED),
    6: ("FRONT PROXY FAILURE: rproxy-0", RED),
    7: ("BACK PROXY FAILURE: rproxy-1 and rproxy-2", RED),
    8: ("BACKEND HOST UNREACHABLE", RED),
    9: ("APPLICATION FAILURE", RED),
    10: ("FRONT PROXY DEGRADED: TLS / HTTP / auth on rproxy-0", YELLOW),
    11: ("DEGRADED: partial or slow (see component health)", YELLOW),
    12: ("EXTERNAL PATH FAILURE: Cloudflare cannot reach origin", RED),
    13: ("BACK PROXY LINK FAILURE: rproxy-0 cannot reach rproxy-1/2", RED),
}
DIAG_MAP = [{"type": "value", "options": {
    str(k): {"text": v[0], "color": v[1], "index": i} for i, (k, v) in enumerate(DIAG.items())}}]
OVERALL_MAP = [
    {"type": "value", "options": {"0": {"text": "HEALTHY", "color": GREEN, "index": 0}}},
    {"type": "range", "options": {"from": 10, "to": 11, "result": {"text": "DEGRADED", "color": YELLOW, "index": 1}}},
    {"type": "range", "options": {"from": 1, "to": 9, "result": {"text": "DOWN", "color": RED, "index": 2}}},
    {"type": "range", "options": {"from": 12, "to": 13, "result": {"text": "DOWN", "color": RED, "index": 3}}},
]
UPDOWN_MAP = [{"type": "value", "options": {
    "1": {"text": "UP", "color": GREEN, "index": 0},
    "0": {"text": "DOWN", "color": RED, "index": 1}}}]
GRAY_THRESH = {"mode": "absolute", "steps": [{"color": GRAY, "value": None}]}

_ref = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def target(expr, legend="__auto", instant=True, fmt="time_series", ref=None):
    return {"datasource": DS, "expr": expr, "legendFormat": legend, "instant": instant,
            "range": not instant, "format": fmt, "refId": ref or next(_ref)}


def reset_refs():
    global _ref
    _ref = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


panel_id = 0


def panel(ptype, title, x, y, w, h, targets, **kw):
    global panel_id
    panel_id += 1
    reset_refs()
    p = {"id": panel_id, "type": ptype, "title": title, "datasource": DS,
         "gridPos": {"x": x, "y": y, "w": w, "h": h}, "targets": targets}
    p.update(kw)
    return p


def row(title, y, collapsed=False):
    global panel_id
    panel_id += 1
    return {"id": panel_id, "type": "row", "title": title, "collapsed": collapsed,
            "gridPos": {"x": 0, "y": y, "w": 24, "h": 1}, "panels": []}


def stat(title, x, y, w, h, targets, mappings=None, unit=None, thresholds=None, desc=None,
         text_mode="value", color_mode="background", no_value="UNKNOWN", decimals=None, overrides=None,
         orientation="auto", text_size=None):
    defaults = {"mappings": mappings or [], "thresholds": thresholds or GRAY_THRESH,
                "color": {"mode": "thresholds"}, "noValue": no_value}
    if unit:
        defaults["unit"] = unit
    if decimals is not None:
        defaults["decimals"] = decimals
    opts = {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
            "colorMode": color_mode, "graphMode": "none", "justifyMode": "center",
            "textMode": text_mode, "orientation": orientation, "wideLayout": True,
            "showPercentChange": False}
    if text_size:
        opts["text"] = text_size
    return panel("stat", title, x, y, w, h, targets, description=desc or "",
                 fieldConfig={"defaults": defaults, "overrides": overrides or []}, options=opts)


panels = []
y = 0

# ------------------------------------------------------------------ 1. Service overview
panels.append(row("Service overview", y)); y += 1
panels.append(stat(
    "Service", 0, y, 4, 4,
    [target(f'max by (vhost) (probe_success{{{J},{SVC},vhost!=""}})', "{{vhost}}")],
    text_mode="name", color_mode="none", no_value="$service",
    desc="Virtual host probed for the selected $service."))
panels.append(stat(
    "Overall status", 4, y, 3, 4,
    [target(f'service_path:probable_failure_code{{{SVC}}}')], mappings=OVERALL_MAP,
    desc="HEALTHY / DEGRADED / DOWN, derived from service_path:probable_failure_code. UNKNOWN = no probe data."))
panels.append(stat(
    "External path", 7, y, 3, 4,
    [target(f'service_path:path_health{{{SVC},path="external"}}')], mappings=NODE_MAP,
    desc="Worst hop on Public DNS -> Cloudflare -> rproxy-0 -> back proxies -> host -> app."))
panels.append(stat(
    "Internal path", 10, y, 3, 4,
    [target(f'service_path:path_health{{{SVC},path="internal"}}')], mappings=NODE_MAP,
    desc="Worst hop on Internal DNS -> rproxy-0 -> back proxies -> host -> app."))
http_thresh = {"mode": "absolute", "steps": [
    {"color": RED, "value": None}, {"color": GREEN, "value": 200}, {"color": YELLOW, "value": 300},
    {"color": "orange", "value": 400}, {"color": RED, "value": 500}]}
panels.append(stat(
    "HTTP status (via back proxy)", 13, y, 3, 4,
    [target(f'max(probe_http_status_code{{{J},{SVC},role="back_proxy_primary",probe_type="http"}})')],
    mappings=[{"type": "value", "options": {"0": {"text": "no response", "color": RED, "index": 0}}}],
    thresholds=http_thresh, decimals=0,
    desc="Status code returned when the application health path is requested through the primary back proxy "
         "with the service's Host header. 502/504 = proxy is up but cannot reach the backend."))
panels.append(stat(
    "Response time (via Cloudflare)", 16, y, 3, 4,
    [target(f'max(probe_duration_seconds{{{J},{SVC},component="cloudflare"}})')], unit="s",
    thresholds={"mode": "absolute", "steps": [{"color": GREEN, "value": None}, {"color": YELLOW, "value": 1},
                                              {"color": RED, "value": 3}]},
    color_mode="value", no_value="n/a",
    desc="Full external round trip: DNS-independent request to the Cloudflare edge, Cloudflare -> origin -> "
         "rproxy-0 (stops at the oauth2 sign-in for authenticated sites)."))
panels.append(stat(
    "Probable failure location", 19, y, 5, 4,
    [target(f'service_path:probable_failure_code{{{SVC}}}')], mappings=DIAG_MAP,
    desc="Inferred from the per-hop probes (first matching rule wins, see Failure summary). "
         "This is a probable location, not a proven root cause.",
    text_size={"valueSize": 18}))
y += 4

# ------------------------------------------------------------------ 2. Service path canvas
panels.append(row("Service path", y)); y += 1

elements = []


def box(cx, top, w=16, h=12):
    return {"left": cx - w / 2, "right": 100 - (cx + w / 2), "top": top, "bottom": 100 - (top + h)}


SCALE = {"horizontal": "scale", "vertical": "scale"}


def conn(target_name, src, dst, field, kind, standby=False):
    """kind = hop (state line) or flow (animated overlay)."""
    if kind == "hop":
        return {"source": {"x": src[0], "y": src[1]}, "target": {"x": dst[0], "y": dst[1]},
                "targetName": target_name, "path": "straight",
                "color": {"field": f"hop_{field}", "fixed": "rgba(142,142,142,0.45)"},
                "size": {"fixed": 7, "min": 1, "max": 10},
                "direction": {"fixed": "none"},
                "lineStyle": {"style": "dashed" if standby else "solid", "animate": False}}
    return {"source": {"x": src[0], "y": src[1]}, "target": {"x": dst[0], "y": dst[1]},
            "targetName": target_name, "path": "straight",
            "color": {"field": f"flow_{field}", "fixed": "transparent"},
            "size": {"fixed": 2, "min": 1, "max": 10},
            "direction": {"fixed": "forward"},
            "lineStyle": {"style": "dashed", "animate": True}}


def node(name, field, title, subtitle, cx, top, links=()):
    conns = []
    for (tname, src, dst, efield, standby) in links:
        conns.append(conn(tname, src, dst, efield, "hop", standby))
        conns.append(conn(tname, src, dst, efield, "flow", standby))
    elements.append({
        "type": "rectangle", "name": name,
        "config": {"text": {"mode": "template" if "$" in title else "fixed", "fixed": title}, "color": {"fixed": INK},
                   "size": 15, "align": "center", "valign": "top"},
        "constraint": SCALE, "placement": box(cx, top),
        "background": {"color": {"field": field, "fixed": GRAY}},
        "border": {"color": {"fixed": "rgba(0,0,0,0.35)"}, "width": 1, "radius": 8},
        "connections": conns})
    # Status line inside the box (words, so the diagram does not depend on colour alone)
    pl = box(cx, top)
    pl["top"] = top + 5
    elements.append({
        "type": "text", "name": f"{name}_status",
        "config": {"text": {"mode": "field", "field": field, "fixed": "NO DATA"}, "color": {"fixed": INK},
                   "size": 13, "align": "center", "valign": "middle"},
        "constraint": SCALE, "placement": pl,
        "background": {"color": {"fixed": "transparent"}}, "border": {"color": {"fixed": "transparent"}},
        "connections": []})
    pl2 = box(cx, top)
    pl2["top"] = top + 8.5
    elements.append({
        "type": "text", "name": f"{name}_sub",
        "config": {"text": {"mode": "fixed", "fixed": subtitle}, "color": {"fixed": "rgba(17,18,23,0.75)"},
                   "size": 10, "align": "center", "valign": "middle"},
        "constraint": SCALE, "placement": pl2,
        "background": {"color": {"fixed": "transparent"}}, "border": {"color": {"fixed": "transparent"}},
        "connections": []})


def label(name, text_cfg, left, top, width, height, size=12, color=GRAY, align="center"):
    elements.append({
        "type": "text", "name": name,
        "config": {"text": text_cfg, "color": color if isinstance(color, dict) else {"fixed": color}, "size": size, "align": align, "valign": "middle"},
        "constraint": SCALE,
        "placement": {"left": left, "right": 100 - (left + width), "top": top, "bottom": 100 - (top + height)},
        "background": {"color": {"fixed": "transparent"}}, "border": {"color": {"fixed": "transparent"}},
        "connections": []})


def hop_label(edge, left, top):
    label(f"lbl_{edge}", {"mode": "field", "field": f"hop_{edge}", "fixed": ""}, left, top, 9, 4, size=11)


# Layout (percent of the panel). x = column centre, top = row top.
X_EXT, X_MID, X_INT, X_BP1, X_BP2, X_APP = 16, 50, 84, 32, 68, 84
R_DNS, R_CF, R_FP, R_BP, R_HOST = 6, 26, 40, 60, 82

label("hdr_ext", {"mode": "fixed", "fixed": "EXTERNAL"}, X_EXT - 10, 0, 20, 5, size=13)
label("hdr_int", {"mode": "fixed", "fixed": "INTERNAL"}, X_INT - 10, 0, 20, 5, size=13)
label("diagnosis", {"mode": "field", "field": "diagnosis", "fixed": "No probe data"}, 30, 0, 40, 6, size=15,
      color={"field": "diagnosis", "fixed": GRAY})
label("legend", {"mode": "fixed", "fixed":
                 "Box = component state · thick line = hop state (grey = not tested) · "
                 "moving dashes = hop currently carrying traffic · dashed = standby path"},
      0, 95, 100, 5, size=10)

node("n_public_dns", "public_dns", "Public DNS", "1.1.1.1 / 8.8.8.8", X_EXT, R_DNS,
     [("n_cloudflare", (0, -1), (0, 1), "dns_edge", False)])
node("n_cloudflare", "cloudflare", "Cloudflare", "public edge, HTTPS", X_EXT, R_CF,
     [("n_rproxy0", (1, -0.4), (-1, 0.3), "edge_front", False)])
node("n_internal_dns", "internal_dns", "Internal DNS", "Pi-hole dns-0 / dns-1", X_INT, R_DNS,
     [("n_rproxy0", (0, -1), (1, 0.3), "idns_front", False)])
node("n_rproxy0", "front_proxy", "rproxy-0", "front proxy, TLS + oauth2", X_MID, R_FP,
     [("n_rproxy1", (-0.5, -1), (0, 1), "front_bp1", False),
      ("n_rproxy2", (0.5, -1), (0, 1), "front_bp2", True)])
node("n_rproxy1", "back_proxy_primary", "rproxy-1", "back proxy (primary)", X_BP1, R_BP,
     [("n_host", (0, -1), (-0.6, 1), "bp1_host", False)])
node("n_rproxy2", "back_proxy_standby", "rproxy-2", "back proxy (standby)", X_BP2, R_BP,
     [("n_host", (0, -1), (0.6, 1), "bp2_host", True)])
node("n_host", "host", "Backend host", "ping or app port", X_MID, R_HOST,
     [("n_app", (1, 0), (-1, 0), "host_app", False)])
node("n_app", "app", "Application", "health endpoint", X_APP, R_HOST)

hop_label("dns_edge", X_EXT + 1, 19.5)
hop_label("edge_front", 30, 32)
hop_label("idns_front", 66, 27)
hop_label("front_bp1", 34, 53)
hop_label("front_bp2", 57, 53)
hop_label("bp1_host", 33, 74)
hop_label("bp2_host", 58, 74)
hop_label("host_app", 62, 84)

canvas_overrides = [
    {"matcher": {"id": "byRegexp", "options": "hop_.*"},
     "properties": [{"id": "mappings", "value": HOP_MAP}]},
    {"matcher": {"id": "byRegexp", "options": "flow_.*"},
     "properties": [{"id": "mappings", "value": FLOW_MAP}]},
    {"matcher": {"id": "byName", "options": "diagnosis"},
     "properties": [{"id": "mappings", "value": [{"type": "value", "options": {
         k: {"text": "Probable failure location: " + v["text"], "color": v["color"], "index": v["index"]}
         for k, v in DIAG_MAP[0]["options"].items()}}]}]},
]
reset_refs()
canvas = panel(
    "canvas", "Service path: $service", 0, y, 24, 17,
    [target(f'service_path:node_health{{{SVC}}}', "{{node}}", ref="A"),
     target(f'service_path:edge_health{{{SVC}}}', "hop_{{edge}}", ref="B"),
     target(f'service_path:edge_flow{{{SVC}}}', "flow_{{edge}}", ref="C"),
     target(f'service_path:probable_failure_code{{{SVC}}}', "diagnosis", ref="D")],
    description=(
        "Each box is coloured by its own probe (green OK, yellow degraded/slow, red failed, grey no data). "
        "Each thick line is the state of that hop; grey means the hop could not be tested (an earlier hop "
        "failed or there is no data). Moving dashes appear only on hops that should currently carry "
        "traffic: rproxy-2 is an nginx `backup` upstream and only carries traffic when rproxy-1 is down."),
    fieldConfig={"defaults": {"mappings": NODE_MAP, "thresholds": GRAY_THRESH,
                              "color": {"mode": "thresholds"}},
                 "overrides": canvas_overrides},
    options={"inlineEditing": False, "showAdvancedTypes": True, "panZoom": False, "infinitePan": False,
             "root": {"type": "frame", "name": "Element root", "elements": elements,
                      "background": {"color": {"fixed": "transparent"}},
                      "border": {"color": {"fixed": "transparent"}},
                      "constraint": {"horizontal": "left", "vertical": "top"},
                      "placement": {"left": 0, "top": 0, "width": 100, "height": 100},
                      "connections": []}})
panels.append(canvas)
y += 17

# ------------------------------------------------------------------ 3. Component health
panels.append(row("Component health", y)); y += 1
reset_refs()
comp_targets = []
for node_name, title in [("public_dns", "Public DNS"), ("internal_dns", "Internal DNS"),
                         ("cloudflare", "Cloudflare / public endpoint"), ("front_proxy", "rproxy-0"),
                         ("back_proxy_primary", "rproxy-1"), ("back_proxy_standby", "rproxy-2"),
                         ("host", "$service host"), ("app", "$service application")]:
    comp_targets.append(target(f'service_path:node_health{{{SVC},node="{node_name}"}}', title))
panels.append(stat("Component health", 0, y, 24, 4, comp_targets, mappings=NODE_MAP, text_mode="value_and_name",
                   desc="Per-component state from the service_path:node_health recording rule.",
                   orientation="vertical"))
y += 4
reset_refs()
corroborate = [
    target('up{job="node",instance="$backend"}', "node_exporter on {{instance}}"),
    target('nginx_up', "nginx on {{instance}}"),
    target('rproxy_backend_reachable', "{{instance}} → {{backend}} :80"),
    target('rproxy_backend_endpoint_up{site="$fqdn"}', "{{instance}} → backend :{{port}}"),
    target('rproxy_oauth2_proxy_port_up{site="$fqdn"}', "oauth2-proxy on {{instance}}"),
]
panels.append(stat(
    "Corroborating signals (existing exporters)", 0, y, 24, 4, corroborate, mappings=UPDOWN_MAP,
    text_mode="value_and_name", orientation="vertical", no_value="no data",
    desc="Signals that already existed before the service path probes: node_exporter, nginx-prometheus-exporter "
         "and the rproxy textfile health checks (refreshed every 5 minutes on the proxies). These are measured "
         "from the proxies themselves, so they confirm or contradict what the central probes see."))
y += 4

# ------------------------------------------------------------------ 4. Probe details
panels.append(row("Probe details", y)); y += 1
reset_refs()
panels.append(panel(
    "state-timeline", "Probe results over time", 0, y, 24, 9,
    [target(f'probe_success{{{J},{SVC}}}', "{{instance}}", instant=False)],
    description="probe_success for every hop probe of $service. Use this to see which hop failed first.",
    fieldConfig={"defaults": {"mappings": [{"type": "value", "options": {
        "1": {"text": "OK", "color": GREEN, "index": 0}, "0": {"text": "FAIL", "color": RED, "index": 1}}}],
        "thresholds": GRAY_THRESH, "color": {"mode": "thresholds"}, "custom": {"fillOpacity": 80, "lineWidth": 0}},
        "overrides": []},
    options={"showValue": "never", "rowHeight": 0.85, "mergeValues": True, "alignValue": "left",
             "legend": {"showLegend": False, "displayMode": "list", "placement": "bottom"},
             "tooltip": {"mode": "single", "sort": "none"}}))
y += 9

reset_refs()
by = "instance, component, probe_type, path, target"
table_targets = [
    target(f'max by ({by}) (probe_success{{{J},{SVC}}})', fmt="table", ref="A"),
    target(f'max by ({by}) (probe_duration_seconds{{{J},{SVC}}})', fmt="table", ref="B"),
    target(f'max by ({by}) (probe_http_status_code{{{J},{SVC}}})', fmt="table", ref="C"),
    target(f'max by ({by}) (probe_dns_lookup_time_seconds{{{J},{SVC}}})', fmt="table", ref="D"),
    target(f'max by ({by}) (probe_http_duration_seconds{{{J},{SVC},phase="connect"}})', fmt="table", ref="E"),
    target(f'max by ({by}) (probe_http_duration_seconds{{{J},{SVC},phase="tls"}})', fmt="table", ref="F"),
    target(f'max by ({by}) (probe_http_duration_seconds{{{J},{SVC},phase="processing"}})', fmt="table", ref="G"),
    target(f'max by ({by}) ((probe_ssl_earliest_cert_expiry{{{J},{SVC}}} - time()) / 86400)', fmt="table",
           ref="H"),
]
col = {"Value #A": "Success", "Value #B": "Probe duration", "Value #C": "HTTP status",
       "Value #D": "DNS lookup", "Value #E": "TCP connect", "Value #F": "TLS handshake",
       "Value #G": "HTTP processing", "Value #H": "Cert days left"}
table_overrides = [
    {"matcher": {"id": "byName", "options": "Success"}, "properties": [
        {"id": "mappings", "value": UPDOWN_MAP}, {"id": "custom.cellOptions", "value": {"type": "color-background"}}]},
    {"matcher": {"id": "byName", "options": "HTTP status"}, "properties": [
        {"id": "unit", "value": "none"}, {"id": "decimals", "value": 0},
        {"id": "thresholds", "value": http_thresh},
        {"id": "custom.cellOptions", "value": {"type": "color-text"}}]},
    {"matcher": {"id": "byName", "options": "Cert days left"}, "properties": [
        {"id": "unit", "value": "d"}, {"id": "decimals", "value": 0},
        {"id": "thresholds", "value": {"mode": "absolute", "steps": [
            {"color": RED, "value": None}, {"color": YELLOW, "value": 7}, {"color": GREEN, "value": 21}]}},
        {"id": "custom.cellOptions", "value": {"type": "color-text"}}]},
]
for name in ["Probe duration", "DNS lookup", "TCP connect", "TLS handshake", "HTTP processing"]:
    table_overrides.append({"matcher": {"id": "byName", "options": name},
                            "properties": [{"id": "unit", "value": "s"}, {"id": "decimals", "value": 3}]})
panels.append(panel(
    "table", "Current probe details", 0, y, 24, 10, table_targets,
    description="Latest result of every probe for $service. HTTP phases and certificate expiry exist only for "
                "HTTP(S) probes; DNS lookup is the resolve phase of HTTP probes (0 when the target is an IP).",
    fieldConfig={"defaults": {"custom": {"align": "auto", "filterable": False}, "thresholds": GRAY_THRESH,
                              "noValue": ""},
                 "overrides": table_overrides},
    options={"showHeader": True, "cellHeight": "sm", "sortBy": [{"displayName": "path", "desc": False}]},
    transformations=[
        {"id": "merge", "options": {}},
        {"id": "organize", "options": {
            "excludeByName": {"Time": True},
            "indexByName": {"path": 0, "component": 1, "probe_type": 2, "instance": 3, "Value #A": 4,
                            "Value #C": 5, "Value #B": 6, "Value #D": 7, "Value #E": 8, "Value #F": 9,
                            "Value #G": 10, "Value #H": 11, "target": 12},
            "renameByName": col}}]))
y += 10


def ts(title, x, w, expr, legend, unit="s", desc="", stack=False):
    reset_refs()
    return panel("timeseries", title, x, y, w, 8, [target(expr, legend, instant=False)], description=desc,
                 fieldConfig={"defaults": {"unit": unit, "custom": {
                     "drawStyle": "line", "lineWidth": 1, "fillOpacity": 10 if not stack else 60,
                     "showPoints": "never", "spanNulls": False,
                     "stacking": {"mode": "normal" if stack else "none", "group": "A"}},
                     "color": {"mode": "palette-classic"}}, "overrides": []},
                 options={"legend": {"showLegend": True, "displayMode": "table", "placement": "right",
                                     "calcs": ["lastNotNull", "max"]},
                          "tooltip": {"mode": "multi", "sort": "desc"}})


panels.append(ts("Probe duration (all hops)", 0, 12,
                 f'probe_duration_seconds{{{J},{SVC}}}', "{{instance}}",
                 desc="probe_duration_seconds: total time of each probe (DNS query, TCP connect, ICMP round trip, "
                      "or full HTTP request)."))
panels.append(ts("DNS resolution time", 12, 12,
                 f'probe_duration_seconds{{{J},{SVC},probe_type="dns"}}', "{{instance}}",
                 desc="Duration of the DNS probes against public and internal resolvers."))
y += 8
panels.append(ts("HTTP phase breakdown", 0, 12,
                 f'probe_http_duration_seconds{{{J},{SVC},phase=~"connect|tls|processing|transfer"}}',
                 "{{instance}} {{phase}}", stack=True,
                 desc="probe_http_duration_seconds by phase: connect = TCP connect, tls = TLS handshake, "
                      "processing = time to first byte (server/upstream time), transfer = body."))
panels.append(ts("HTTP status codes", 12, 12,
                 f'probe_http_status_code{{{J},{SVC}}}', "{{instance}}", unit="none",
                 desc="probe_http_status_code; 0 = no HTTP response (connection or TLS failure)."))
y += 8
panels.append(ts("TCP / ICMP reachability time", 0, 12,
                 f'probe_duration_seconds{{{J},{SVC},probe_type=~"tcp|icmp"}}', "{{instance}}",
                 desc="TCP connect and ICMP round-trip probe durations."))
panels.append(ts("TLS certificate days remaining", 12, 12,
                 f'(probe_ssl_earliest_cert_expiry{{{J},{SVC}}} - time()) / 86400', "{{instance}}", unit="d",
                 desc="Earliest certificate expiry seen on the HTTPS probes (rproxy-0 origin cert and the "
                      "Cloudflare edge cert)."))
y += 8

# ------------------------------------------------------------------ 5. Failure summary
panels.append(row("Failure summary", y)); y += 1
panels.append(stat(
    "Probable failure location", 0, y, 10, 5,
    [target(f'service_path:probable_failure_code{{{SVC}}}')], mappings=DIAG_MAP,
    desc="Probable location only: inferred from which hops fail, not a proven root cause.",
    text_size={"valueSize": 26}))
reset_refs()
panels.append(panel(
    "state-timeline", "Probable failure location over time", 10, y, 14, 5,
    [target(f'service_path:probable_failure_code{{{SVC}}}', "$service", instant=False)],
    fieldConfig={"defaults": {"mappings": DIAG_MAP, "thresholds": GRAY_THRESH, "color": {"mode": "thresholds"},
                              "custom": {"fillOpacity": 80, "lineWidth": 0}}, "overrides": []},
    options={"showValue": "auto", "rowHeight": 0.8, "mergeValues": True, "alignValue": "left",
             "legend": {"showLegend": False, "displayMode": "list", "placement": "bottom"},
             "tooltip": {"mode": "single", "sort": "none"}}))
y += 5
logic_md = """\
**How the probable failure location is chosen** (first match wins; from `service_path:probable_failure_code`):

| # | Condition | Shown as |
|---|---|---|
| 1 | Public **and** internal DNS failing | DNS FAILURE |
| 2 | rproxy-0 unreachable from the LAN but Cloudflare still reaches it | INTERNAL PATH FAILURE (LAN → rproxy-0) |
| 3 | rproxy-0 failing (TCP 443 closed) | FRONT PROXY FAILURE |
| 4 | rproxy-0 cannot reach rproxy-1 **and** rproxy-2 (measured on rproxy-0) | BACK PROXY LINK FAILURE |
| 5 | rproxy-1 **and** rproxy-2 down | BACK PROXY FAILURE |
| 6 | Backend host does not answer ping or the app port | BACKEND HOST UNREACHABLE |
| 7 | Host up, health endpoint failing | APPLICATION FAILURE |
| 8 | Only internal DNS failing / wrong answer | INTERNAL PATH FAILURE (DNS) |
| 9 | Only public DNS failing / private answer leaked | EXTERNAL PATH FAILURE (DNS) |
| 10 | Cloudflare returns 52x (origin unreachable) while rproxy-0 is fine from the LAN | EXTERNAL PATH FAILURE (Cloudflare → origin) |
| 11 | Cloudflare edge unreachable / TLS failure | EXTERNAL PATH FAILURE (edge) |
| 12 | rproxy-0 answers TCP but HTTPS/vhost/oauth2 check fails | FRONT PROXY DEGRADED |
| 13 | Anything partial or slow (one DNS server, standby proxy, slow hop) | DEGRADED |

**Probe limits.** On oauth2-protected sites, the Cloudflare and rproxy-0 probes stop at the oauth2-proxy sign-in page. They prove the edge, TLS, the vhost and oauth2-proxy, but not the backend. The backend is tested separately through rproxy-1 and rproxy-2 (same Host header). The Cloudflare probe starts inside the LAN and leaves through the home WAN, so a WAN outage shows up as an external path failure.
"""
reset_refs()
panels.append(panel("text", "Diagnosis logic", 0, y, 24, 12, [], options={"mode": "markdown", "content": logic_md},
                    datasource=None))
y += 12

dashboard = {
    "uid": "service-path",
    "title": "Service Path",
    "description": "Per-hop request path health (DNS, Cloudflare, rproxy-0/1/2, backend host, application) "
                   "for homelab services. Answers: where does the request path stop working?",
    "tags": ["blackbox", "observability", "web", "service-path"],
    "editable": True,
    "graphTooltip": 1,
    "schemaVersion": 41,
    "version": 1,
    "refresh": "30s",
    "time": {"from": "now-6h", "to": "now"},
    "timepicker": {},
    "timezone": "browser",
    "fiscalYearStartMonth": 0,
    "liveNow": False,
    "links": [{"title": "Web service status", "type": "link", "url": "/d/web-service-status", "icon": "dashboard",
               "targetBlank": False, "tooltip": "", "asDropdown": False, "includeVars": False,
               "keepTime": True, "tags": []}],
    "annotations": {"list": [{"builtIn": 1, "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                              "enable": True, "hide": True, "iconColor": "rgba(0, 211, 255, 1)",
                              "name": "Annotations & Alerts", "type": "dashboard"}]},
    "templating": {"list": [
        {"name": "service", "label": "Service", "type": "query", "datasource": DS,
         "query": {"query": 'label_values(probe_success{job="service_path"}, service)', "refId": "service"},
         "definition": 'label_values(probe_success{job="service_path"}, service)',
         "refresh": 2, "sort": 1, "multi": False, "includeAll": False,
         "current": {"text": "lidarr", "value": "lidarr"}, "options": [], "hide": 0},
        {"name": "fqdn", "label": "Virtual host", "type": "query", "datasource": DS,
         "query": {"query": 'label_values(probe_success{job="service_path",service="$service",vhost!=""}, vhost)',
                   "refId": "fqdn"},
         "definition": 'label_values(probe_success{job="service_path",service="$service",vhost!=""}, vhost)',
         "refresh": 2, "sort": 1, "multi": False, "includeAll": False, "current": {}, "options": [], "hide": 2},
        {"name": "backend", "label": "Backend host", "type": "query", "datasource": DS,
         "query": {"query": 'label_values(probe_success{job="service_path",service="$service"}, backend)',
                   "refId": "backend"},
         "definition": 'label_values(probe_success{job="service_path",service="$service"}, backend)',
         "refresh": 2, "sort": 1, "multi": False, "includeAll": False, "current": {}, "options": [], "hide": 2},
    ]},
    "panels": panels,
}

output = os.path.normpath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)
with open(output, "w", encoding="utf-8") as fh:
    json.dump(dashboard, fh, indent=2)
print("wrote", output)
print("panels:", len(panels), "canvas elements:", len(elements))
