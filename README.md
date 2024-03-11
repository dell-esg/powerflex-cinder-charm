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

## Deployment

This charm's primary use is as a backend for the cinder charm. To do so, add a relation betweeen both charms:

    juju integrate cinder-powerflex:storage-backend cinder:storage-backend


# Documentation

The OpenStack Charms project maintains two documentation guides:

* [OpenStack Charm Guide][cg]: for project information, including development
  and support notes
* [OpenStack Charms Deployment Guide][cdg]: for charm usage information

[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/charm-cinder-solidfire/+filebug).
