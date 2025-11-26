# Role: `pve`

## 📖 Overview
Contains tasks to manage the Proxmox Virtual Environment

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (bookworm)

## 🧮 Defaults
- `pve_ceph_pool_name`: `cephfs_data_pool`
- `pve_ceph_pool_pg_num`: `128`
- `pve_ceph_storage_id`: `cephfs_data`
- `pve_ceph_storage_type`: `ceph`
- `pve_ceph_storage_pool`: `"{{ pve_ceph_pool_name }}"`
- `pve_ceph_storage_content`: `images,rootdir`
- `pve_ceph_storage_nodes`: `"{{ groups['pve_nodes'] }}"`
- `pve_ceph_storage_max_backups`: `1`
- `pve_ceph_storage_enabled`: `1`
- `pve_ceph_storage_shared`: `1`
- `pve_ceph_storage_path`: `""`
- `pve_ceph_storage_options`: `"monhost={{ groups['ceph_nodes'] | map('extract', hostvars, ['ansible_host']) | join(',') }}"`
- `pve_ceph_storage_prune_backups`: `0`
- `pve_ceph_storage_prune_interval`: `0`
- `pve_ceph_storage_prune_keep_last`: `0`
- `pve_ceph_storage_prune_keep_hourly`: `0`
- `pve_ceph_storage_prune_keep_daily`: `0`
- `pve_ceph_storage_prune_keep_weekly`: `0`
- `pve_ceph_storage_prune_keep_monthly`: `0`
- `pve_ceph_storage_prune_keep_yearly`: `0`
- `pve_ceph_storage_prune_exclude`: `""`
- `pve_ceph_storage_comment`: `"Ceph RBD Storage"`
- `pve_ceph_network_cidr`: `"10.0.2.0/24"`
- `pve_ceph_network_bridge`: `vmbr1`
- `pve_ceph_network_bridge_ports`: `enp4s0`
- `pve_ceph_public_network`: `"{{ pve_ceph_network_cidr }}"`
- `pve_ceph_cluster_network`: `"{{ pve_ceph_network_cidr }}"`
- `pve_ceph_osd_disks`: `['/dev/sda']  # Only using one disk per node for Ceph OSDs but can be adjusted as needed.`
- `pve_ceph_rbd_storage_id`: `cephfs_storage`
- `pve_oidc_realm`: `azure.refol.us`

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
_No tasks defined._

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: pve
```