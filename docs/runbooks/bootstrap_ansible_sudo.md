# Bootstrap Passwordless Sudo on a Manually Created VM

Use this runbook to prepare an existing Linux VM that was created manually, rather than provisioned through Ansible. SSH access alone does not configure passwordless sudo. Before privileged automation can run, the `ansible` account needs a working sudo rule on the VM.

The examples target `ansible-1` using `inventory/ansible/inventory.ini`. Substitute the correct host and inventory for another VM. Run controller commands from the repository root; run guest commands only on the intended VM. Execute steps individually and stop on errors.

## 1. Understand the Bootstrap Requirement

Ansible cannot create a root-owned sudoers file without first obtaining root privileges. The [node preparation playbook](../../playbooks/ansible/prep_ansible_node.yml) uses `become: true`, so it requires either working password-based sudo or existing passwordless sudo.

This procedure mirrors the passwordless-sudo tasks in the [ansible_node role](../../roles/ansible_node/tasks/main.yml): ensure group `ansible` exists, append the intended users to that group with `/bin/bash` as their shell, create `/etc/sudoers.d` with mode `0755`, and install `%ansible ALL=(ALL) NOPASSWD:ALL` in `/etc/sudoers.d/99_ansible` with mode `0440` and `visudo` validation. It covers the sudo bootstrap, not the role's separate remote temporary-directory setup.

| Option                    | Purpose                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| `-k`, `--ask-pass`        | Prompt locally for the SSH login password.                                |
| `-K`, `--ask-become-pass` | Prompt locally for the sudo password, which Ansible sends to remote sudo. |

These are separate authentication steps, even if the passwords are identical. `-K` does not bypass sudo authentication. An error such as `Timeout (12s) waiting for privilege escalation prompt` means the expected sudo exchange did not complete; it does not by itself prove the password or sudoers rule is wrong.

If interactive `sudo su` works but Ansible escalation does not, use the manual bootstrap below. Repeatedly running a privileged playbook cannot bypass that initial authentication problem.

## 2. Establish Administrative Access

Prerequisites:

- The VM has an existing `ansible` account and the `sudo` package installed.
- You can SSH to the VM as `ansible` and authenticate with a key or password.
- You know its current sudo password, or have another approved administrator/root console session.
- Passwordless root access for members of group `ansible` is approved. `NOPASSWD:ALL` allows every command as root; review group membership and protect these accounts' credentials accordingly.

From the controller:

```bash
ssh -t ansible@ansible-1
```

On the VM, confirm the account, then open a root shell:

```bash
id ansible
sudo su -
```

Enter the current sudo password interactively. If `ansible` is not permitted to sudo, use another authorized administrator or the VM console. Do not enable remote root SSH just for this procedure. Keep this root shell open until a separate SSH session passes all verification steps.

## 3. Install the Sudoers Rule Manually

In the root shell on the VM, record the account's existing groups and shell for recovery. Ensure group `ansible` exists and append the user without removing its other group memberships:

```bash
id ansible
getent passwd ansible
getent group ansible || groupadd ansible
usermod -aG ansible -s /bin/bash ansible
```

The role also adds the controller's `$USER` (falling back to `SUDO_USER`) and users from `ansible_node_custom_sudo_users` to this group. That list defaults to `semaphore`. The commands above explicitly bootstrap the remote `ansible` account; add other approved accounts only when required. Do not assume the controller's `$USER` names the remote SSH account.

Create the include directory and back up any existing rule outside that directory:

```bash
install -d -o root -g root -m 0755 /etc/sudoers.d
backup_dir="$(mktemp -d /root/ansible-sudo-backup.XXXXXX)"
if [[ -f /etc/sudoers.d/99_ansible ]]; then
  cp -a /etc/sudoers.d/99_ansible "$backup_dir/99_ansible"
fi
printf 'Backup directory: %s\n' "$backup_dir"
visudo -f /etc/sudoers.d/99_ansible
```

Record the backup directory for rollback. In the editor, add the following rule, then save and exit:

```sudoers
%ansible ALL=(ALL) NOPASSWD:ALL
```

The leading `%` means group `ansible`, not user `ansible`. Preserve unrelated lines and avoid adding duplicate rules. Use `visudo` rather than editing sudoers with an unvalidated shell redirect.

Still as root:

```bash
chown root:root /etc/sudoers.d/99_ansible
chmod 0440 /etc/sudoers.d/99_ansible
visudo -cf /etc/sudoers.d/99_ansible
visudo -c
```

Require a successful validation of the complete configuration. Confirm `/etc/sudoers.d/99_ansible` appears among the checked files. If it is not included, inspect `/etc/sudoers` with `visudo` and ensure it contains an active `@includedir /etc/sudoers.d` directive (older configurations may use `#includedir /etc/sudoers.d`). Do not blindly append duplicate directives. Revalidate after any correction.

## 4. Verify Without Cached Authentication

Leave the root recovery shell open. From a separate controller terminal, open a new SSH session so the added group membership takes effect:

```bash
ssh -t ansible@ansible-1
```

In this new session, as user `ansible`, run:

```bash
whoami
id -nG
sudo -k -n /usr/bin/id -u
```

Expected results: `whoami` prints `ansible`, `id -nG` includes group `ansible`, and the sudo command prints `0` with no password prompt. Here `-k` ignores cached sudo authentication and `-n` fails instead of prompting. A working `sudo su` alone is not proof of passwordless sudo.

If verification fails, use the retained root shell to run `visudo -c` and `sudo -l -U ansible`. Check the session's group membership, that the rule uses `%ansible`, and that it is included and not overridden by a later matching rule requiring a password. Sudoers uses matching-rule order, not simply the most specific rule. Review corrections through `visudo`; do not remove unrelated policies or disable PAM to suppress the failure.

If earlier troubleshooting installed `/etc/sudoers.d/99_ansible_user`, review it separately: that user-specific grant is independent of the role's group rule and can mask a missing group membership. The role does not manage or remove that file.

## 5. Verify Through Ansible

Once the guest-side passwordless check succeeds, run this non-mutating test from the controller. It deliberately omits `-K`:

```bash
ansible \
  -i inventory/ansible/inventory.ini ansible-1 \
  -u ansible -k --become \
  -m ansible.builtin.raw -a 'id -u'
```

The result must be successful and print `0`. `-k` is still needed if SSH itself uses a password; passwordless sudo does not configure SSH keys. Omit `-k` when key-based SSH works.

If guest-side verification succeeds but Ansible still times out, repeat the raw test with `--timeout 60 -vvv` and inspect the SSH/sudo exchange. A longer timeout can help with slow authentication, but cannot bypass a policy denial or missing credentials. Redact sensitive details before sharing diagnostic output; never put passwords in command arguments, committed variables, or this runbook.

## 6. Prepare the Existing VM for First Use

After sudo verification succeeds, run the post-creation playbooks in the same order as [the VM provisioning playbook](../../playbooks/provision_vm.yml). Do not run that wrapper or its `vms/provision_vm.yml` import against this manually created VM: the VM already exists. Run each command separately and require success before continuing.

Before proceeding:

- Confirm the selected host belongs to the inventory's `vms` and `python` groups. `--limit` restricts a play's targets but does not add a host to its required groups; an empty/skipped play is not successful preparation.
- Review the host's Python version and virtual-environment settings, domain/DNS settings and domain credentials, `users_list`, and `disks_disk_mounts`. Supply vault credentials through the repository's normal workflow; add `--ask-vault-pass` to commands if needed. Do not put secret values in command arguments.
- These Python and domain roles target Ubuntu/APT-based guests. Confirm compatibility with the manually installed OS before applying them.
- Keep console access available. Domain join changes DNS/authentication configuration and reboots the VM. User setup can change passwords, shells, home directories, and group membership. Back up existing configuration and data before applying these changes.

The commands retain `-k` for password-based SSH and omit `-K` because passwordless sudo is now configured. Omit `-k` when SSH keys work.

### 6.1 Bootstrap Python

Run [the Python bootstrap playbook](../../playbooks/python/bootstrap_python3.yml) first. It uses raw commands for early tasks, installs the configured Python version, and creates the virtual environment needed by subsequent playbooks.

```bash
ansible-playbook \
  -i inventory/ansible/inventory.ini \
  playbooks/python/bootstrap_python3.yml \
  --limit ansible-1 -u ansible -k
```

Confirm the resulting virtual environment matches the interpreter configured for this inventory/repository. The remaining commands intentionally use that configured interpreter, rather than forcing `/usr/bin/python3` for every playbook.

### 6.2 Join the Domain

Run [the domain join playbook](../../playbooks/ad/join_domain.yml) once the intended domain, DNS servers, and vault-backed `ad_administrator_password` are configured. Expect the VM to reboot; wait for the playbook to finish and SSH access to return before continuing. For a deliberately standalone VM, omit this step only as an explicit departure from the repository's standard provisioning sequence.

```bash
ansible-playbook \
  -i inventory/ansible/inventory.ini \
  playbooks/ad/join_domain.yml \
  --limit ansible-1 -u ansible -k
```

### 6.3 Prepare the Ansible Node

Run [the node preparation playbook](../../playbooks/ansible/prep_ansible_node.yml) to apply the full `ansible_node` role, including group membership, the sudoers rule, and the remote temporary directory. Include `ansible` explicitly in the custom user list rather than relying on the controller's `$USER`; this example also preserves the default `semaphore` entry. Preserve any additional inventory-specific users when overriding this list.

```bash
ansible-playbook \
  -i inventory/ansible/inventory.ini \
  playbooks/ansible/prep_ansible_node.yml \
  --limit ansible-1 -u ansible -k \
  -e '{"ansible_node_custom_sudo_users":["semaphore","ansible"]}'
```

### 6.4 Configure Users

Review `users_list` before running [the user setup playbook](../../playbooks/vms/add_users.yml). Its group assignment replaces supplementary memberships when `user.groups` is specified; preserve group `ansible` for accounts relying on the group sudo rule. Account/password changes must preserve a tested administrative login.

```bash
ansible-playbook \
  -i inventory/ansible/inventory.ini \
  playbooks/vms/add_users.yml \
  --limit ansible-1 -u ansible -k
```

### 6.5 Prepare Disks Only After Storage Review

The final import in the reference sequence is [the disk preparation playbook](../../playbooks/vms/prep_disk.yml). Do not run it blindly on an existing VM. The [disks role](../../roles/disks/tasks/main.yml) can rewrite `/etc/fstab`, partition disks without child devices, format partitions as ext4, and mount unmounted ext4 partitions using `disks_disk_mounts`. A disk without child partitions is not necessarily empty: it may contain a whole-disk filesystem or other data.

Inspect the existing layout from the controller:

```bash
ssh ansible@ansible-1 'lsblk -f'
ssh ansible@ansible-1 'cat /etc/fstab'
```

Require a verified backup, reviewed device selections and mount mappings, and approval for any formatting or mount changes. If existing storage is already configured or the role's automatic selection does not match the intended disks, skip this step and document that decision rather than risking existing data. Only after that review, run:

```bash
ansible-playbook \
  -i inventory/ansible/inventory.ini \
  playbooks/vms/prep_disk.yml \
  --limit ansible-1 -u ansible -k
```

### 6.6 Confirm Readiness

Open a fresh SSH session and repeat the group-membership and uncached passwordless-sudo checks in section 4, especially after user setup. From the controller, verify that normal Python-based modules work through the configured interpreter:

```bash
ansible \
  -i inventory/ansible/inventory.ini ansible-1 \
  -u ansible -k --become -m ansible.builtin.ping
```

Require a successful `pong` response. Confirm domain membership if domain join was performed, expected user access, and intended mounts if disk preparation was performed. Record any intentionally skipped steps before proceeding to service deployment.

## 7. Recovery and Rollback

Keep the root recovery shell open until both guest-side and Ansible verification succeed. If configuration validation fails, repair it through `visudo` before disconnecting.

To roll back from that root shell, restore the previous `99_ansible` file from the recorded backup directory if one existed. If the file was newly created, remove only `/etc/sudoers.d/99_ansible`. Restore the account's previous shell and remove its `ansible` group membership only if this procedure added it and rollback requires doing so; preserve all pre-existing memberships. Do not delete a group used by other accounts. Run `visudo -c` again and verify the original administrative access still works. Removing the group rule affects every member who relied on it and can restore the sudo password requirement, so do not close the recovery session until access is confirmed.
