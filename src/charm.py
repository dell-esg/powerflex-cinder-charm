#! /usr/bin/env python3

# Copyright 2024 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid
import logging

from ops.main import main
from ops_openstack.plugins.classes import CinderStoragePluginCharm

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

VOLUME_DRIVER = 'cinder.volume.drivers.dell_emc.powerflex.driver.PowerFlexDriver'


class CinderPowerflexCharm(CinderStoragePluginCharm):
    
    PACKAGES = ['cinder-common']
    # Overriden from the parent. May be set depending on the charm's properties
    stateless = False
    active_active = False

    mandatory_config = [
        'san-ip', 'san-login', 'san-password'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stored.is_started = True

    def cinder_configuration(self, charm_config) -> 'list[tuple]':
        """Return the configuration to be set by cinder"""
        cget = charm_config.get

        volume_backend_name = cget(
            'volume-backend-name') or self.framework.model.app.name

        raw_options = [
            ('volume_driver', VOLUME_DRIVER),
            ('volume_backend_name', volume_backend_name),
            ('san_ip', cget('san-ip')),
            ('san_login', cget('san-login')),
            ('san_password', cget('san-password')),
            ('powerflex_storage_pools', cget('powerflex-storage-pools')),
            ('powerflex_max_over_subscription_ratio', cget(
                'powerflex-max-over-subscription-ratio')),
            ('san_thin_provision', cget('san-thin-provision')),
            ('powerflex_allow_migration_during_rebuild', cget(
                'powerflex-allow-migration-during-rebuild')),
            ('powerflex_allow_non_padded_volumes', cget(
                'powerflex-allow-non-padded-volumes')),
            ('powerflex_rest_server_port', cget('powerflex-rest-server-port')),
            ('powerflex_round_volume_capacity', cget(
                'powerflex-round-volume-capacity')),
            ('rest_api_connect_timeout', cget('rest-api-connect-timeout')),
            ('rest_api_read_timeout', cget('rest-api-read-timeout'))
        ]
        options = [(x, y) for x, y in raw_options if y]
        return options

if __name__ == "__main__": 
    main(CinderPowerflexCharm)
