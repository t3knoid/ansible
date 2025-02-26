rproxy_setup
----------

rproxy_setup configures reverse proxy with failover support using nginx. This role requires at least three hosts to be defined. One host is configure as the main frontend proxy, the other two acts as the primary and secondary proxy. 

        [rproxy_main]
        rproxy-0

        [rproxy_primary]
        rproxy-1

        [rproxy_secondary]
        rproxy-2

Requirements
------------

This role requires the following roles:

- global
- nginx_setup

It also requires that certificates are deployed into the main reverse proxy host. See the following playbooks.

- playbooks/certs/generate_certs.yml
- playbooks/certs/stage_certs.yml
