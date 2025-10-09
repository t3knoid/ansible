# Create an Ubuntu 24 Virtual Machine in Proxmox Using Ansible

- [Introduction](#introduction)
- [Create a Virtual Machine in Proxmox](#create-a-virtual-machine-in-proxmox)
- [Autoinstall](#autoinstall)
  - [Prepare Autoinstall](#prepare-autoinstall)
    - [Add CD/DVD Drive to Base Virtual Machine](#add-cddvd-drive-to-base-virtual-machine)
    - [Cloud-init ISO Image](#cloud-init-iso-image)
      - [user-data file](#user-data-file)
  - [Manage the Autoinstall Process](#manage-the-autoinstall-process)
    - [Automate Acknowledge Continue of autoinstall](#automate-acknowledge-continue-of-autoinstall)
    - [Wait for autoinstall to complete](#wait-for-autoinstall-to-complete)
- [References](#references)

## Introduction

The following documents the process of automating the deployment of an Ubuntu 24 virtual machine in Proxmox using Ansible. The ansible role automates the process of creating a virtual machine in Proxmox and using [autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) to deploy Ubuntu 24 into the virtual machine.

The tasks in the role are purposedly broken up into three YAML files. This allows customizability and reusability of tasks for use with other playbooks.

- [create.yml](tasks/create.yml) - These tasks creates the base virtual machine in Proxmox.
- [autoinstall.yml](tasks/autoinstall.yml) - These tasks manage the Autoinstall process.
- [cloud_init_iso.yml](tasks/cloud_init_iso.yml) - These tasks creates the Cloud-Init ISO required by Autoinstall.

## Create a Virtual Machine in Proxmox

Creating a virtual machine in Proxmox is straightforward by using the [community.proxmox.proxmox_kvm](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html) module. The virtual machine creation tasks are in the [create.yml](tasks/create.yml) file. As you can see from the code, it is simply filling in the parameters needed by the proxmox_kvm module.

```yaml
- name: Create new ubuntu virtual machine
  community.proxmox.proxmox_kvm:
    api_host: "{{ global_proxmox_api_host }}"
    api_user: "{{ global_proxmox_api_user }}"
    api_password: "{{ global_proxmox_api_password }}"
    node: "{{ vms_proxmox_node | string }}"
    name: "{{ vms_name | default(inventory_hostname) }}"
    agent: "{{ vms_config.agent | string }}"
    storage: "{{ vms_config.storage }}"
    scsihw: "{{ vms_config.scsihw }}"
    net:
      net0: "virtio,bridge=vmbr0"
    virtio:
      virtio0: "{{ vms_config.disk_os.storage }}:{{ vms_config.disk_os.size }}"
    ide:
      ide2: "none,media=cdrom"
    cpu: "{{ vms_config.cpu }}"
    cores: "{{ vms_config.cores | string }}"
    sockets: "{{ vms_config.sockets | int }}"
    memory: "{{ vms_config.memory | int }}"
    ostype: "{{ vms_config.ostype }}"
    state: present
  delegate_to: localhost
  register: vms_new_vm_info
```

The variable, *vms_config* is used to provide [configuration values](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html#parameters) in order to have the ability to customize the virtual machine for any given inventory.

>[!TIP]
> Global variables (prefixed with *global_*) are loaded using a separate role named [global](../global/tasks/main.yml). This role takes care of any variables (including sensitive variables stored in a vault) global to all roles.

```yaml
---

vms_config:
  agent: "1"
  cores: "4"
  cpu: host
  memory: 2048
  ostype: l26
  scsihw: virtio-scsi-single
  sockets: 1
  storage: linstor_storage
  disk_os:
    backup: true
    size: 20
    storage: linstor_storage
  disk2:
    backup: true
    size: 20
    storage: linstor_storage

vms_os: ubuntu_24_server
vms_autoinstall: true
```

Notice that the second CD/DVD drive is not added in this task. This is added later when configuring autoinstall. The rest of the base virtual machine creation is to add an optional hard drive, and mounting the Ubuntu 23 ISO image.

>[!IMPORTANT]
> The Ubuntu 24 ISO installer image](<https://releases.ubuntu.com/>) must be available in the Proxmox node's local storage.

## Autoinstall

Automating Autoinstall has several tasks. The tasks have two main goals; (1) Prepare the virtual machine to run Autoinstall and (2) Manage the Autoinstall process.

The Autoinstall tasks are isolated in its own task file, [autoinstall.yml](tasks/autoinstall.yml). The tasks that creates the Cloud-Init ISO image are located in a separate file, [cloud_init_iso.yml](tasks/cloud_init_iso.yml).

### Prepare Autoinstall

Autoinstall relies on [Cloud-init to provide its configuration](https://canonical-subiquity.readthedocs-hosted.com/en/latest/explanation/cloudinit-autoinstall-interaction.html#cloudinit-autoinstall-interaction). It uses an ISO image that contains [configuration](https://canonical-subiquity.readthedocs-hosted.com/en/latest/tutorial/creating-autoinstall-configuration.html) files autoinstall requires. The Cloud-init ISO image is mounted on a separate CD/DVD device in the virtual machine.

#### Add CD/DVD Drive to Base Virtual Machine

The first task is to add a CD/DVD drive to the base virtual machine image. The task uses he [community.proxmox.proxmox_disk](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_disk_module.html) module.

```yaml
- name: Add second cd-rom drive for cloud-init.iso 
  community.proxmox.proxmox_disk:
    api_host: "{{ global_proxmox_api_host }}"
    api_user: "{{ global_proxmox_api_user }}"
    api_token_id: "{{ global_proxmox_api_token_id }}"
    api_token_secret: "{{ global_proxmox_api_token }}"
    api_password: "{{ global_proxmox_api_password }}"
    vmid: "{{ vms_new_vm_info.vmid | int }}"
    disk: ide0
    media: cdrom
    iso_image: "none"
    state: present
  delegate_to: localhost
```

#### Cloud-init ISO Image

The Cloud-init ISO image contains two files, [userdata](templates/user-data.j2) and meta-data. Both are located in the root of the ISO image. The tasks involve in managing the Cloud-init ISO is located in [cloud_init_iso.yml](tasks/cloud_init_iso.yml) file.

##### user-data file

The user-data file contains the [autoinstall configuration](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html) used to configure the Ubuntu installer. A jinja template file is used to generate the user-data file.

```yaml
#cloud-config
autoinstall:
  version: 1
  locale: en_US
  keyboard:
    layout: us
    variant: ""
    toggle: null
  identity:
    hostname: ubu24-template
    realname: 'Template user'
    username: '{{ global_template_user }}'
    password: '{{ global_template_user_crypted_password }}'
  storage:
    layout:
      name: lvm
      sizing-policy: all
  source:
    id: ubuntu-server-minimal
  network:
    version: 2
    ethernets:
      ens18:
        dhcp4: true
  ssh:
    install-server: yes
    allow-pw: true
    authorized-keys: 
      - "{{ ssh_key.public_key }}"
  packages:
    - vim
    - net-tools
    - realmd
    - sssd
    - sssd-tools
    - libnss-sss
    - libpam-sss
    - adcli
    - samba-common-bin
    - oddjob
    - oddjob-mkhomedir
    - packagekit
    - qemu-guest-agent
  late-commands:
    - echo "%ansible ALL=(ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)
```

>[!TIP]
> Be thoughtful when creating this file in order to create an optimal virtual machine template that provides a good base to clone new virtual machines from.

### Manage the Autoinstall Process

At this point, the Autoprocess is ready to execute the next time the virtual machine is rebooted. Although Autoinstall is designed to be zero-touch, by default it prompts the user with the following to start Autoinstall during reboot.

```bash
Continue with autoinstall? (yes|no)
```

The user must physically answer 'yes' and hit enter in order to continue with installation. One approach to avoid this prompt is to modify the Ubuntu installation ISO by [passing the kernel option *autoinstall*](https://canonical-subiquity.readthedocs-hosted.com/en/latest/explanation/zero-touch-autoinstall.html). This would mean having to modify the iso image.

#### Automate Acknowledge Continue of autoinstall

A more practical approach is to automate the keypresses necessary to acknowledge this prompt. This is accomplished by using the [Proxmox QEMU API](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/qemu/{vmid}/monitor) to send SendKey commands to the virtual machine console during reboot.

To do this, a [Python script](templates/send_yes_to_vm_console.py.j2) is created. When executed, it sends the required keystrokes on the virtual machine console to acknowledge the prompt.

```yaml
- name: Generate Python script to send 'yes' to VM console
  ansible.builtin.template:
    src: send_yes_to_vm_console.py.j2
    dest: /tmp/send_yes_to_vm_console.py
  register: python_script_generated
  delegate_to: localhost

- name: Make the Python script executable
  file:
    path: /tmp/send_yes_to_vm_console.py
    mode: '0755'
  when: python_script_generated.changed
  delegate_to: localhost
```

> **NOTE:**
> This script is executed after the virtual machine has rebooted and the console is sitting at the *Continue with autoinstall? (yes|no)* prompt. Currently the script uses an indeterminate assumption of waiting for this prompt by pausing for two minutes.

#### Wait for autoinstall to complete

To wait for autoinstall to complete, a RESTful call to determine the virtual machine address is repeated until it successful.

```yaml
- name: Wait for VM to fully start by trying to get it's IP address
  ansible.builtin.uri:
    url: 'https://{{ global_proxmox_api_host }}:8006/api2/json/nodes/{{ vms_proxmox_node }}/qemu/{{ vms_new_vm_info.vmid | int }}/agent/network-get-interfaces'
    method: GET
    headers:
      Authorization: "PVEAPIToken={{ global_proxmox_api_user }}!{{ global_proxmox_api_token_id }}={{ global_proxmox_api_token }}"
    follow_redirects: safe
    validate_certs: false
  retries: 30
  delay: 30
  until: result.status == 200
  register: result
  delegate_to: localhost
```

> **NOTE:**
> This is probably not the most elegant way of doing this, but it works. One idea to determine status is to connect to the virtual machine's console serial to read the installer's log output.

## References

- [Deploy Ubuntu 24.04 (Noble Numbat) with Autoinstall to Proxmox](https://sekureco42.ch/posts/deploy-ubuntu-24.04-with-autoinstall-to-proxmox/)
- [Introduction to autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html)
- [community.proxmox.proxmox_kvm](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html)
- [community.proxmox.proxmox_disk](https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_disk_module.html)
- [Proxmox QEMU Monitor API](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/qemu/{vmid}/monitor)
