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

import json
import ops
import ops.testing
import unittest

from charm import CinderPowerflexCharm
from ops.model import BlockedStatus
from unittest.mock import patch


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = ops.testing.Harness(CinderPowerflexCharm)
        self.harness.set_leader(True)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.charm = self.harness.charm

    @patch("ops_openstack.plugins.classes.CinderStoragePluginCharm.on_install")
    @patch.object(CinderPowerflexCharm, "create_connector")
    @patch.object(CinderPowerflexCharm, "install_sdc")
    def test_on_install_missing_relation(self, _install_sdc, _create_connector, _on_install):
        """Test the unit goes to a blocked status when the storage-backend relation is missing."""
        self.charm.on.install.emit()

        _on_install.assert_called_once()
        _install_sdc.assert_called_once()
        _create_connector.assert_called_once()
        self.assertIsInstance(self.harness.model.unit.status, BlockedStatus)

    def test_cinder_configuration(self):
        """Test the cinder_configuration returns correct output based on charm config."""
        # Note, the hooks don't need to fire during this test. Simply disabling the hooks
        # will ensure there's no undesired side effects from the update_config calls.
        self.harness.disable_hooks()
        self.harness.update_config(
            {
                "powerflexgw-ip": "192.123.0.2",
                "powerflexgw-login": "my_admin",
                "powerflexgw-password": "my_password",
            }
        )
        results = dict(self.charm.cinder_configuration(self.charm.config))
        self.assertEqual(
            results["volume_driver"],
            "cinder.volume.drivers.dell_emc.powerflex.driver.PowerFlexDriver",
        )
        self.assertEqual(results["volume_backend_name"], "powerflex")
        self.assertEqual(results["san_ip"], "192.123.0.2")
        self.assertEqual(results["san_login"], "my_admin")
        self.assertEqual(results["san_password"], "my_password")

        # Update the volume_backend_name and ensure it is reflected
        self.harness.update_config({"volume-backend-name": "test"})
        results = dict(self.charm.cinder_configuration(self.charm.config))
        self.assertEqual(results["volume_backend_name"], "test")

        # Update the thin provisioning and rest port ensure its updated. Note these
        # values return non-string return values so are good for validating the results
        # returned aren't unintentionally removed
        self.harness.update_config(
            {
                "powerflex-san-thin-provision": False,
                "powerflex-rest-server-port": 1234,
            }
        )
        results = dict(self.charm.cinder_configuration(self.charm.config))
        self.assertEqual(results["san_thin_provision"], False)
        self.assertEqual(results["powerflex_rest_server_port"], 1234)

    def test_relation_changed(self):
        """Tests that the cinder backend is presented as stateless but not active/active."""
        rel_id = self.harness.add_relation(
            "storage-backend", "cinder-volume", unit_data={"nonce": ""}
        )

        data = self.harness.get_relation_data(rel_id, self.charm.unit.name)
        self.maxDiff = None
        self.assertEqual(
            data,
            {
                "active_active": str(False),
                "backend_name": self.charm.app.name,
                "stateless": str(True),
                "subordinate_configuration": json.dumps(
                    {
                        "cinder": {
                            "/etc/cinder/cinder.conf": {
                                "sections": {
                                    "cinder-dell-powerflex": [
                                        [
                                            "volume_driver",
                                            "cinder.volume.drivers.dell_emc.powerflex.driver.PowerFlexDriver",
                                        ],
                                        [
                                            "volume_backend_name",
                                            self.charm.config["volume-backend-name"],
                                        ],
                                        ["san_login", self.charm.config["powerflexgw-login"]],
                                        [
                                            "san_password",
                                            self.charm.config["powerflexgw-password"],
                                        ],
                                        [
                                            "powerflex_storage_pools",
                                            self.charm.config["powerflex-storage-pools"],
                                        ],
                                        [
                                            "powerflex_max_over_subscription_ratio",
                                            self.charm.config[
                                                "powerflex-max-over-subscription-ratio"
                                            ],
                                        ],
                                        [
                                            "san_thin_provision",
                                            self.charm.config["powerflex-san-thin-provision"],
                                        ],
                                        [
                                            "powerflex_allow_migration_during_rebuild",
                                            self.charm.config[
                                                "powerflex-allow-migration-during-rebuild"
                                            ],
                                        ],
                                        [
                                            "powerflex_allow_non_padded_volumes",
                                            self.charm.config[
                                                "powerflex-allow-non-padded-volumes"
                                            ],
                                        ],
                                        [
                                            "powerflex_rest_server_port",
                                            self.charm.config["powerflex-rest-server-port"],
                                        ],
                                        [
                                            "powerflex_round_volume_capacity",
                                            self.charm.config["powerflex-round-volume-capacity"],
                                        ],
                                        [
                                            "rest_api_connect_timeout",
                                            self.charm.config[
                                                "powerflex-rest-api-connect-timeout"
                                            ],
                                        ],
                                        [
                                            "rest_api_read_timeout",
                                            self.charm.config["powerflex-rest-api-read-timeout"],
                                        ],
                                    ]
                                }
                            }
                        }
                    }
                ),
            },
        )

    @patch("charmhelpers.core.host.mkdir")
    @patch("charm.render")
    def test_create_connector(self, _render, _mkdir):
        """Test the connector renders non-replication settings."""
        self.harness.disable_hooks()
        self.charm.create_connector()

        _mkdir.assert_called_once_with("/opt/emc/scaleio/openstack")
        _render.assert_called_once_with(
            source="connector.conf",
            target="/opt/emc/scaleio/openstack/connector.conf",
            context = ({"backends": {"cinder_name": "cinder-dell-powerflex",
                                     "san_password": "password"}}),
            perms=0o600,
        )

    @patch("charmhelpers.core.host.mkdir")
    @patch("charm.render")
    def test_create_connector_with_replication(self, _render, _mkdir):
        """Test the connector renders replication settings."""
        self.harness.update_config(
            {
                "powerflex-replication-config": (
                    "backendid:acme,san_ip:10.20.30.41,san_login:admin,san_password:password"
                )
            }
        )
        _render.reset_mock()
        self.charm.create_connector()
        _render.assert_called_once_with(
            source="connector.conf",
            target="/opt/emc/scaleio/openstack/connector.conf",
            context={
                "backends": {
                    "cinder_name": "cinder-dell-powerflex",
                    "san_password": "password",
                    "rep_san_password": "password",
                }
            },
            perms=0o600,
        )
