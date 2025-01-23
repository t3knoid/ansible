# Autofs

The autofs role is used to install and configure autofs. It currently supports nfs mounts.

## Requirements

The role requires initializing the *autofs_nfs_mounts* variable. This variable is a list of mount points.

## Role variables

- autofs_nfs_mounts - a list of dictionaries. Each item defines the required parameters for each mountpoint.

```bash
  - mount_name: music
    server: 192.168.2.250:/mnt/Data/music
    mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
  - mount_name: downloads
    server: 192.168.2.250:/mnt/Data/downloads/complete
    mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
  - mount_name: incomplete-downloads
    server: 192.168.0.250:/mnt/Data/downloads/incomplete
    mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
```

## Dependencies

None

## Example Playbook

```bash
- name: Deploy autofs
  hosts: all
  become: true
  roles:
    - autofs
  vars:
    autofs_nfs_mounts:
      - mount_name: music
        server: 192.168.2.250:/mnt/Data/music
        mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
      - mount_name: downloads
        server: 192.168.2.250:/mnt/Data/downloads/complete
        mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
      - mount_name: incomplete-downloads
        server: 192.168.0.250:/mnt/Data/downloads/incomplete
        mount_options: -rw,relatime,hard,rsize=1048576,wsize=1048576,proto=tcp,timeo=600,retrans=2,sec=sys
```