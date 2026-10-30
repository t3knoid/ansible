# 🗄️ Migrate a PostgreSQL Instance Between Hosts

Use this runbook to migrate a PostgreSQL instance's logical databases and approved roles from one host to another. Source and destination can be VMs, physical servers, or supported PostgreSQL containers/Apps. The destination must already be provisioned and accessible. This is an operator-led logical dump/restore migration, not a physical cluster copy, an in-place upgrade, or an automatic migration playbook. The document keeps its historical filename so existing links continue to work.

For a complete instance move, inventory every database, role, and consumer and stop all writers before taking the final database set. All final dumps must represent the same frozen application state. For selected databases moving into an existing shared instance, select a complete application/database dependency set and leave unrelated databases alone. Per-database dumps are individually consistent but do not provide a cross-database snapshot while writers continue running.

Run Ansible commands from the repository root. Run PostgreSQL client commands from a secured migration workstation with network access to both servers. Execute commands individually and stop on errors; do not execute the entire document as a script. Never point restore commands at a database containing data you intend to keep. A separate optional example at the end covers `pg-1` and the TrueNAS destination.

## 📋 1. Establish Scope and Recovery Requirements

| Item                    | Required Decision                                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------------- |
| Source instance         | Verified hostname/IP, port, PostgreSQL major version, and instance identity                        |
| Target instance         | Different verified endpoint/instance, supported version, storage, and administration access        |
| Migration scope         | Entire instance or an explicitly reviewed set of related databases and consumers                   |
| Database mapping        | Source/target names, owners, encodings, collations, extensions, and any target collisions          |
| Role mapping            | Required login/owner/group roles, memberships, credentials, privileges, and role/database settings |
| Downtime strategy       | Stop and fence all writers in the migration scope through final dump, restore, and cutover         |
| Acceptance and rollback | Agreed checks, retention period, recovery owner, and handling of writes made after cutover         |

- Obtain owner approval, an outage window, backup retention, recovery objectives, and a tested restore. Keep an independent copy of backups outside the source and target failure domains.
- Do not decommission the source, remove its inventory/IP/DNS, or delete source databases during migration. Keep working administrative access to both systems.
- Freeze unrelated application/image upgrades, deployments, scheduled jobs, and automatic updates that could restart writers or alter schema. If PostgreSQL major versions differ, review all intervening compatibility changes and rehearse that upgrade as part of this migration.
- Confirm adequate target CPU/memory/storage, extension support, and connection capacity. Establish monitoring and a PostgreSQL-aware backup/restore policy before production cutover.
- Treat related application databases as one unit, including main/log pairs. For a full instance move, discover every non-template database and every consumer; an application inventory is not proof of a complete database inventory.

## 🔎 2. Discover Source Databases and Compatibility

Use client tools matching the target major version, provided that `pg_dump` version supports the source release. For example, PostgreSQL 18 client tools can perform a supported older-source-to-18 migration without upgrading the source first. Verify server and client versions; do not use an older `pg_dump` against a newer source or assume downgrade restores are supported. Use the same client-tool installation for dump, archive inspection, restore, and SQL checks to avoid PATH selecting another version.

Create a fresh private workspace on the migration workstation. Replace endpoint placeholders before connecting. Configure a `0600` password file privately with exact host/port/database/user entries; do not put passwords in shell arguments or connection URIs. Account for all databases used by the commands. The destination administration login must be capable of creating the approved roles, databases, and extensions.

```bash
umask 077
MIGRATION_DIR="$(mktemp -d "$HOME/postgresql-migration.XXXXXX")" && export MIGRATION_DIR
export SOURCE_HOST='<verified-source-endpoint>'
export SOURCE_PORT=5432
export SOURCE_ADMIN='<approved-source-backup-login>'
export TARGET_HOST='<verified-target-endpoint>'
export TARGET_PORT=5432
export TARGET_ADMIN='<approved-target-administration-login>'
export SOURCE_MAINT_DB=postgres
export TARGET_MAINT_DB=postgres
export PGPASSFILE="${MIGRATION_DIR:?Create the private migration workspace first}/pgpass"
install -m 0600 /dev/null "$PGPASSFILE"
```

Populate that password file using your approved private editor/secret workflow. Entries use `hostname:port:database:username:password`; escape colons/backslashes in credentials according to PostgreSQL's password-file rules and cover each required connection. Never paste the populated file into a ticket or source control. The source may not permit remote administrative login; arrange approved restricted access or an SSH tunnel rather than opening superuser access broadly. All following commands use `--no-password` to fail instead of prompting. Set maintenance database names to existing databases available to the respective administrator, and use the appropriate TLS/certificate policy for each endpoint; do not disable verification merely to connect.

```bash
pg_dump --version
pg_restore --version
psql --version
psql -X --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" -d "$SOURCE_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT version(), inet_server_addr(), inet_server_port();"
psql -X --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" -d "$TARGET_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT version(), inet_server_addr(), inet_server_port();"
psql -X --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" -d "$SOURCE_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT datname, pg_get_userbyid(datdba) AS owner, pg_encoding_to_char(encoding) AS encoding, datcollate, datctype, pg_database_size(oid) AS bytes FROM pg_database WHERE NOT datistemplate ORDER BY datname;"
psql -X --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" -d "$SOURCE_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin, rolreplication, rolbypassrls FROM pg_roles ORDER BY rolname;"
psql -X --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" -d "$SOURCE_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT datname, usename, application_name, client_addr, state FROM pg_stat_activity WHERE backend_type = 'client backend' ORDER BY datname, usename;"
```

For each candidate database, set its exact verified name and inspect extensions and application data:

```bash
export SOURCE_DB='<verified-application-database>'
psql -X --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" -d "$SOURCE_DB" -v ON_ERROR_STOP=1 -c "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
psql -X --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" -d "$TARGET_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT name, default_version, installed_version FROM pg_available_extensions ORDER BY name;"
```

Also record locale provider/collation versions, custom tablespaces, large objects, FDWs/external servers, publications/subscriptions, scheduled jobs, connection settings, and required privileges. Foreign-server options can contain secrets; inspect them privately. A container, appliance, or managed service may lack source extensions or superuser privileges. Resolve those restrictions through the target's supported management workflow before proceeding; do not assume arbitrary OS package installation is permitted.

Build a reviewed mapping for all databases and roles in scope. Names can collide on an existing target; roles are cluster-wide, including credentials and privileges. Preserve the destination's bootstrap/administrative roles and maintenance databases. Inspect source `postgres` and any customized template databases: a whole-instance migration is incomplete until their required user objects/settings are handled. Do not restore blindly over target maintenance databases or replace built-in templates. Such objects need a separately tested selective migration. Database renaming or owner remapping also needs a tested procedure, not a blind `--create` restore.

## ⚙️ 3. Prepare the Target Instance and Roles

- Provision PostgreSQL through the target platform's approved method before migration. Confirm persistent storage, runtime identity/permissions, the selected port, and backup/restore procedures. Do not unintentionally upgrade or redeploy the working target during restore.
- Configure restricted client access, PostgreSQL authentication, and appropriate TLS. A wildcard listener is not an access-control policy. Test both administrative migration access and application login from their actual networks.
- Create only the required target login/owner/group roles and memberships through an approved database administration workflow. Keep the existing application passwords in vault when possible, so endpoint cutover does not also rotate credentials. Use an interactive `psql` `\password role_name` command in a private session for approved password setup; do not paste plaintext passwords into SQL history.
- Preserve ownership, grants, role memberships, and required role/database settings through reviewed definitions. Do not grant superuser to every application role or restore all source globals over an existing target.
- Record which server settings must be reproduced or deliberately changed, including connection limits, memory, preload libraries, authentication, and extension configuration. Logical dumps do not migrate the server's operating-system/service configuration.
- Update ongoing provisioning and backup plans, not just runtime client config. Choose automation compatible with the target platform; host-delegated APT/systemd roles are not suitable for a remote container or managed database.

Create roles before restoring their owned objects. Use an approved SQL/Ansible workflow for only the required identities, with permissions the target supports. Managed services may require a separately tested ownership/privilege mapping; do not remove ownership/grants from a dump merely to suppress errors without reviewing the resulting access model.

## 💾 4. Rehearse Dumps and Restores

Use a protected review copy of role definitions as evidence, not as an unattended restore script:

```bash
pg_dumpall --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" --database="$SOURCE_MAINT_DB" --globals-only --no-role-passwords --file="$MIGRATION_DIR/source-globals-review.sql"
```

This includes cluster-wide definitions and may reference unsuitable privileges or source tablespaces. Review and selectively reproduce approved roles/memberships/settings; passwords are deliberately excluded and must be supplied through the approved secret workflow. Do not execute this file wholesale on an existing target. Translate required server/authentication settings through target-supported configuration rather than copying source `postgresql.conf`, `pg_hba.conf`, or host ownership blindly.

Rehearse on an isolated test instance or explicitly isolated test database set before the outage. Protect dumps as production data. Check restore duration, extension compatibility, collations, ownership/ACLs, representative row counts, and application operation. A successful `pg_restore --list` is not proof of a successful restore or usable database. Do not run a trial application against the final writable target or allow production jobs/notifications to run from the rehearsal.

Existing backup jobs can supplement the migration backup only after scope review. Some application jobs capture only one database or prune earlier dumps. Verify coverage of every database, roles, external state, and an independent backup copy; do not assume an application's normal backup job migrates an entire instance.

## ⏸️ 5. Quiesce and Fence Source Writers

Stop applications, workers, scripts, scheduled jobs, and deployment automation through their supported service/container/orchestrator controls. Inspect stop/start playbooks before relying on them; stopping a systemd wrapper does not necessarily stop a container. Confirm that automatic restart policies or another administrator cannot resume writers.

For a whole-instance move, stop every writer across all migration databases before any final dump, and keep the source PostgreSQL server running for logical exports. For a selected-database move, fence all writers in that dependency set without interrupting unrelated source databases. Stop writes on any intended target databases until restore/validation completes as well.

Recheck `pg_stat_activity` for the exact database set and inspect `pid`, `xact_start`, and `state_change` when investigating persistent sessions. `idle` still means connected and capable of later writes; it is not proof the application is stopped. The inspection session and monitoring connections may be expected, but must be identified. Check background/replication writers separately. Do not terminate unrelated sessions or apply cluster-wide restrictions to a shared source without approval.

Arrange an approved source-access fence so an old deployment cannot resume writes during or after cutover. Record the freeze point. If writers resume, stop and take new final dumps after restoring a consistent freeze; do not proceed with stale or cross-database-inconsistent exports.

## 📦 6. Take Final Dumps and Restore

Repeat for every approved database in the migration scope, including dependent/log databases. For a complete instance move, finish all final dumps while every source writer remains fenced. Do not use a pre-freeze rehearsal dump for cutover. Custom format includes schema/data, ownership, grants, sequences, and large objects for that database, but not cluster roles or external-system state.

```bash
export SOURCE_DB='<verified-application-database>'
export DUMP_FILE="${MIGRATION_DIR:?}/${SOURCE_DB}.dump"
pg_dump --no-password -h "$SOURCE_HOST" -p "$SOURCE_PORT" -U "$SOURCE_ADMIN" --format=custom --file="$DUMP_FILE" --dbname="$SOURCE_DB"
pg_restore --list "$DUMP_FILE"
sha256sum "$DUMP_FILE"
```

Execute commands individually and require a zero exit status from each. Restrict filesystem permissions, retain checksums, and copy the final dumps and reviewed metadata to the approved independent backup location before proceeding. For unusual database names, choose a safe dump filename explicitly rather than using the name as a path.

The following restore assumes the target database name equals the source name, has no target collision, and is not `postgres`, `template0`, `template1`, or the chosen target maintenance database. Confirm this before running; `--create` creates the database named inside the archive, not a name derived from `--dbname`. All referenced roles must exist, extensions must be available, and locale/provider requirements must be compatible. Review database-level settings that embed role, path, or endpoint names as part of the restore plan.

```bash
psql -X --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" -d "$TARGET_MAINT_DB" -v ON_ERROR_STOP=1 -c "SELECT datname FROM pg_database ORDER BY datname;"
pg_restore --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" --exit-on-error --create --no-tablespaces --dbname="$TARGET_MAINT_DB" "$DUMP_FILE"
```

`--no-tablespaces` deliberately uses destination default storage rather than source-specific tablespace placements. Confirm that capacity/performance policy is acceptable; preserving tablespace layouts requires a separately tested target mapping. This is not an overwrite/drop workflow: do not add `--clean` to clear a collision. A failed restore can leave a partial target database; isolate it, inspect the error, and obtain approval before removing/recreating only that migration-owned target. Do not ignore role, extension, ownership, or collation errors. If the source is untrusted, review dump contents/code before restoring with powerful target privileges.

After a successful restore, reconnect to that target database, update planner statistics, and validate it before enabling writers:

```bash
psql -X --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" -d "$SOURCE_DB" -v ON_ERROR_STOP=1 -c 'ANALYZE;'
psql -X --no-password -h "$TARGET_HOST" -p "$TARGET_PORT" -U "$TARGET_ADMIN" -d "$SOURCE_DB" -v ON_ERROR_STOP=1 -c "SELECT extname, extversion FROM pg_extension ORDER BY extname;"
```

Compare approved table counts/checks, owners, grants, schema objects, sequence behavior, encodings/collations, and large-object access with the frozen source. Verify real application logins can access every required database. For an entire instance, account for all source databases, reviewed globals, maintenance/template customizations, and separately configured external/server state before declaring migration complete. Logical replication is a separate rehearsed strategy for larger workloads/tighter outages; sequences, DDL, large objects, and final writer fencing need explicit treatment.

## 🔀 7. Switch Client Endpoints

After every database in the cutover unit passes validation, update the clients' database hostname/IP, port, and any approved name/credential mappings. Update TLS expectations and related secret/configuration sources. The server's filesystem data directory is not a client connection property. Keep unrelated application versions/settings unchanged.

Use a reviewed configuration/deployment path that cannot provision databases on the wrong host or initialize an existing target. In Ansible, inspect `--syntax-check` and `--list-hosts` with the exact inventory/host limit; delegated tasks and imported database plays still require review. A host limit is not proof that a role has no remote database side effects.

For database-specific DNS aliases, plan TTLs, client caches, TLS certificate names, connection-pool refresh, and rollback behavior. Do not repoint the old server's general-purpose hostname when it still hosts other workloads. Explicitly stop/restart or recycle client pools so existing connections do not remain attached to the source.

Keep source writes fenced and record when the target first accepts production writes. For a whole-instance migration, switch all consumers in the approved plan before declaring success. For staged database moves, update only the migrated clients while unrelated source databases remain in service.

## ✅ 8. Accept or Roll Back the Cutover

- Confirm every migrated client connects to the target, not the source; inspect sessions and client logs on both endpoints and ensure source writers remain fenced.
- Test login/UI/API functionality and representative reads/writes, including log writes and background jobs. Watch connection, memory, disk, and application error metrics.
- Verify backups and monitoring now address the target and perform a restore test to an isolated destination. Existing source-local backup/restore tasks and `.pgpass` entries must not silently continue protecting only the old copy.
- Preserve the unchanged source database set behind the source-access fence for the agreed rollback window. Do not allow active writers on both copies or attempt ad hoc bidirectional merging.

If the target has not accepted writes, stop the cutover application, restore its exact original source endpoint/configuration, remove only the intended source fence, and restart through the reviewed application deployment. Verify it reads/writes the source again. Restoring the endpoint alone does not undo a changed application schema/version.

Once the target has accepted writes, the source is stale. Stop writers and choose an approved reconciliation/data-restore strategy before rollback; simply pointing clients back loses target changes. A reverse logical restore to an older PostgreSQL version is not automatically supported. Capture target backups and evidence before any recovery attempt, and do not destroy the target just to return to the old state.

## 🧹 9. Retire the Source Only After Acceptance and Retention

Account for every source database/consumer, including nonempty maintenance/template customizations. Confirm no sessions, backups, jobs, exporters, replication, or external integrations depend on the source. Update ongoing provisioning so future deployments cannot recreate databases there or point clients back at it. For a partial move, retain the source instance for its remaining workloads instead of decommissioning the host.

Archive migration records, ownership mappings, backup checksums, endpoint changes, validation results, and retention approvals. Delete old databases or decommission the host/DNS/monitoring only through a separate approved manual procedure after the rollback window. Keep old data and backups according to policy; no deletion command is part of this migration.

## 🧩 Optional Homelab Example: `pg-1` to TrueNAS

This is one application of the generic procedure, not its required topology. Consult the [PostgreSQL inventory](../../inventory/pg/inventory.ini), [services inventory](../../inventory/services/inventory.ini), and [TrueNAS App configuration](../../inventory/truenas/host_vars/truenas-01/default.yml). Verify the running versions rather than assuming the inventory is current.

| Generic Input   | Example                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------- |
| `SOURCE_HOST`   | Verified `pg-1` endpoint, normally the VM address or a dedicated database DNS name                |
| `SOURCE_PORT`   | Verified source port, commonly `5432`                                                             |
| `TARGET_HOST`   | TrueNAS App endpoint, normally `192.168.2.250`                                                    |
| `TARGET_PORT`   | Verified published App port, commonly `5432`                                                      |
| `TARGET_ADMIN`  | Approved App administration login, commonly `postgres`                                            |
| Migration units | Sonarr, Radarr, and Lidarr main/log database pairs; discover actual names and any other databases |

The [Apps playbook](../../playbooks/truenas/deploy_truenas_apps.yml) manages the destination container, not database roles or logical migration. The [VM PostgreSQL deployment playbook](../../playbooks/postgresql/deploy_postgresql.yml) and the [same-VM 17-to-18 migration playbook](../../playbooks/postgresql/migrate_postgresql_17_to_18.yml) are not host-to-host migration tools. Do not add the NAS to `pgdb`: existing database tasks assume APT/systemd and a local `postgres` OS account on a VM.

For these applications, review `<service>_setup_db_name`, `<service>_setup_db_log`, `<service>_setup_db_user`, and vault-backed passwords. Set explicit endpoint overrides in only the migrated application's group variables:

| Variables File                                                | Example Overrides                                                     |
| ------------------------------------------------------------- | --------------------------------------------------------------------- |
| [Sonarr](../../inventory/services/group_vars/sonarr/main.yml) | `sonarr_setup_pg_host: "192.168.2.250"`, `sonarr_setup_pg_port: 5432` |
| [Radarr](../../inventory/services/group_vars/radarr/main.yml) | `radarr_setup_pg_host: "192.168.2.250"`, `radarr_setup_pg_port: 5432` |
| [Lidarr](../../inventory/services/group_vars/lidarr/main.yml) | `lidarr_setup_pg_host: "192.168.2.250"`, `lidarr_setup_pg_port: 5432` |

Their role defaults can select `global_ip_addresses[groups['pgdb'][0]]`, so do not rely on group ordering. Review application backup/restore tasks too: some use source-host-local binaries, write source `.pgpass` files, or capture only a main database. Moving the runtime endpoint alone does not migrate provisioning and backup automation.

For Sonarr, inspect the scoped application deployment before using it to render the new endpoint:

```bash
ansible-playbook -i inventory/services/inventory.ini playbooks/services/deploy_sonarr.yml --limit sonarr-0 --syntax-check --ask-vault-pass
ansible-playbook -i inventory/services/inventory.ini playbooks/services/deploy_sonarr.yml --limit sonarr-0 --list-hosts --ask-vault-pass
```

That playbook imports a `pgdb` database-creation play, which must have no selected hosts under the exact app-host limit. Inspect delegated tasks as well; do not let VM database setup run against the source or NAS. These are full application deployments and can pull images, restart containers, or change other settings. Apply only after all database restores pass and that scope is approved; otherwise prepare a separate config-only change. Validate equivalent Radarr/Lidarr workflows independently. Stop/start controls must operate on the actual Docker container, not an unrelated systemd service.

For the TrueNAS target, retain local persistent storage, use the supported App/image extension set, and verify exposed-port/authentication/TLS policy. Do not install OS packages directly on the appliance to compensate for an incompatible database image.

## 🛠️ Automation Follow-Up

There is no dedicated cross-host PostgreSQL migration playbook in this checkout. A future workflow should select one verified source/target and migration scope, reject target collisions, reconcile approved roles over the database connection, capture every required dump, verify checksums/restores, and report cutover readiness. Full-instance scope requires completeness and writer-freeze checks across all databases; selected-database scope must preserve unrelated workloads. Require separate approval for shutdown, endpoint changes, and any later cleanup. Migration must not become a side effect of ordinary database installation or App deployment.
