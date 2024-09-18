Dell PowerFlex Storage Backend for Cinder
-----------------------------------------

## Overview

This charm provides a Dell PowerFlex storage backend for use with the Cinder charm.

## Configuration

This section covers common and/or important configuration options. See file `config.yaml` for the full list of options, along with their descriptions and default values. See the [Juju documentation][juju-docs-config-apps] for details on configuring applications.

### `powerflexgw-ip`

The PowerFlex Gateway IP or hostname.

### `powerflexgw-login`

The username used to access the PowerFlex Gateway

### `powerflexgw-password`

The password used to authenticate to the PowerFlex Gateway

### `powerflex-max-over-subscription-ratio`

Speciifies the maximum oversubscription ratio allowed by the system. If it's not specified, the value of 10.0 will be set.

### `powerflex-thin-provision`

Specifies the provisioning type used when the user asks for a volume. Can be either `thick` or `thin`(default).

### `powerflex-storage-pools`

A comma-separated list of storage pool names to use. Each storage pool must be set under the form of `ProtectionDomain:StoragePool`.

### `powerflex-allow-migration-during-rebuild`

Allows or prevents volume migration during rebuild process. Disabled by default.

### `powerflex-allow-non-padded-volumes`

Allows volumes to be created in a storage pool when zero padding feature is disabled. Disabled by default.

### `powerflex-rest-server-port`

TCP port used to communicate with the PowerFlex Gateway. 443 by default.

### `powerflex-round-volume-capacity`

Allows or prevents the size of a volume to be an increment of 8GB. Enabled by default.

### `powerflex-rest-api-connect-timeout`

Connection timeout value (in seconds) for REST API calls to the PowerFlex Gateway. If not specified, the value of 30s will be set.

### `powerflex-rest-api-read-timeout`

Read timeout value (in seconds) for REST API calls to the PowerFlex Gateway. If not specified, the value of 30s will be set.

### `powerflex-replication-config`

Specifies the settings for enabling the replication. Only one replication is supported for each backend.

### `powerflex-sdc-mdm-ips`

Specifies a comma-separated list of MDM IPs. Can be used to defined a VIP also. This is required during the SDC configuration.

## Deployment

This charm's primary use is as a backend for the cinder charm. To do so, add a relation between both charms:
   
    juju deploy --config cinder-powerflex-config.yaml --resource sdc-deb-package=../EMC-ScaleIO-sdc-4.5-2.185.Ubuntu.22.04.x86_64.deb cinder-powerflex
    juju integrate cinder-powerflex:storage-backend cinder:storage-backend

Depending on the kernel version that your system runs on, you may have to install the proper SDC kernel module.
An alternative method which triggers an on-demand compilation process can be used if your SDC is 3.6.3 and higher or 4.5.2 and higher.
You can refer to the documentation here:
* [On-demand compilation of the PowerFlex SDC driver][sdc]

This charm doesn't include yet the enablement of the on-demand compilation. In case the scini service can't start and your SDC is at version mentioned above, you can enable the feature by creating an empty file on every nodes which runs the SDC driver.
    
    sudo touch /etc/emc/scaleio/scini_sync/.build_scini
    sudo service scini restart

[sdc]: https://www.dell.com/support/kbdoc/en-us/000224134/how-to-on-demand-compilation-of-the-powerflex-sdc-driver


# Documentation

The OpenStack Charms project maintains two documentation guides:

* [OpenStack Charm Guide][cg]: for project information, including development
  and support notes
* [OpenStack Charms Deployment Guide][cdg]: for charm usage information

[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/charm-cinder-powerflex/+filebug).
