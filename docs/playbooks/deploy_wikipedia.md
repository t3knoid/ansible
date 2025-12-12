# 📖 Playbook: wikipedia/deploy_wikipedia.yml

## 🛠 Purpose
Deploys a Wikipedia instance using various setup roles.

## 🔗 Roles Applied
- [`global`](../roles/global/README.md)
- [`lamp_setup`](../roles/lamp_setup/README.md)
- [`mediawiki_setup`](../roles/mediawiki_setup/README.md)
- [`java_setup`](../roles/java_setup/README.md)
- [`elasticsearch_setup`](../roles/elasticsearch_setup/README.md)
- [`wikipedia_setup`](../roles/wikipedia_setup/README.md)

## 🚀 Usage
```bash
ansible-playbook playbooks/wikipedia/deploy_wikipedia.yml
```