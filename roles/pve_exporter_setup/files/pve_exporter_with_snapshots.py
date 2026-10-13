import logging

from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.core import GaugeMetricFamily
from proxmoxer import ProxmoxAPI
from pve_exporter import cli, http


class SnapshotCollector:
    def __init__(self, pve):
        self.pve = pve

    def collect(self):
        timestamps = GaugeMetricFamily(
            "pve_vm_snapshot_created_timestamp_seconds",
            "Creation time of Proxmox VM snapshots in Unix seconds",
            labels=["id", "vmid", "name", "node", "snapshot"],
        )
        success = GaugeMetricFamily(
            "pve_vm_snapshot_collection_success",
            "Whether all local VM snapshots were collected successfully",
        )
        try:
            local_node = next(
                entry["name"] for entry in self.pve.cluster.status.get()
                if entry["type"] == "node" and entry.get("local")
            )
            for vm in self.pve.nodes(local_node).qemu.get():
                if vm.get("template"):
                    continue
                vmid = str(vm["vmid"])
                for snapshot in self.pve.nodes(local_node).qemu(vmid).snapshot.get():
                    if snapshot["name"] == "current":
                        continue
                    timestamps.add_metric(
                        [f"qemu/{vmid}", vmid, vm.get("name", vmid),
                         local_node, snapshot["name"]],
                        snapshot["snaptime"],
                    )
        except Exception:
            logging.getLogger("gunicorn.error").error(
                "Unable to collect all local VM snapshots; check API access and VM.Audit permissions"
            )
            success.add_metric([], 0)
            return [success]
        success.add_metric([], 1)
        return [timestamps, success]


def collect_pve_with_snapshots(config, host, cluster, node, options):
    output = collect_pve(config, host, cluster, node, options)
    if node:
        registry = CollectorRegistry()
        registry.register(SnapshotCollector(ProxmoxAPI(host, **config)))
        output += generate_latest(registry)
    return output


collect_pve = http.collect_pve


if __name__ == "__main__":
    http.collect_pve = collect_pve_with_snapshots
    cli.main()