# Role: `elasticsearch_setup`

## 📖 Overview
Install and configure Elasticsearch on Debian/Ubuntu

## 📋 Requirements
- Minimum Ansible version: `2.9`
- Supported on: `Debian` (buster, bullseye)
- Supported on: `Ubuntu` (noble)

## 🧮 Defaults
- `elasticsearch_setup_version`: `9.1.5`
- `elasticsearch_setup_repo_url`: `"https://artifacts.elastic.co/packages/9.x/apt"`
- `elasticsearch_setup_installer`: `"elasticsearch-{{ elasticsearch_setup_version }}-amd64.deb"`
- `elasticsearch_setup_http_port`: `9200` — Cluster settings
- `elasticsearch_setup_heap_size`: `"1g"`
- `elasticsearch_setup_clustername`: `"my_cluster"`
- `elasticsearch_setup_host`: `"0.0.0.0"`
- `elasticsearch_setup_discoverytype`: `"single-node"`
- `elasticsearch_setup_node_name`: `"{{ inventory_hostname }}"`
- `elasticsearch_setup_config_path`: `"/etc/elasticsearch/elasticsearch.yml"`
- `elasticsearch_setup_data_path`: `"/var/lib/elasticsearch"`
- `elasticsearch_setup_log_path`: `"/var/log/elasticsearch"`
- `elasticsearch_setup_plugins`: ``

## 🧮 Vars
_No constant variables found in vars._

## 🛠 Tasks
- Install dependencies
- Download binary GPG key
- Add Elasticsearch APT repository
- Install specific version of Elasticsearch
- Configure Elasticsearch
- Set JVM heap size
- Install plugins
- Enable and start Elasticsearch

## 🚀 Example Usage
```yaml
- hosts: all
  roles:
    - role: elasticsearch_setup
```