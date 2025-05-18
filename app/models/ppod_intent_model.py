from uuid import UUID as CORE_UUID

from sqlalchemy import Column, DateTime, Integer, String, UUID, func, Text


from app.models.base import Base
from app import schemas


class PpodIntent(Base):
    __tablename__ = "ppod_intent"

    id = Column(Integer, primary_key=True, index=True)
    ppod_intent_id = Column(UUID, nullable=False)
    ppod_intent_name = Column(String(255), nullable=False)
    cpod_intent_id = Column(UUID, nullable=True)
    ref_cpod_intent_id = Column(UUID, nullable=False)
    ref_cpod_intent_name = Column(String(255), nullable=False)

    leaf_uplink_a_lag_ipv4_local = Column(String(255), nullable=True)
    leaf_uplink_a_lag_ipv4_remote = Column(String(255), nullable=True)
    leaf_uplink_a_lag_ipv4_subnet = Column(String(255), nullable=True)
    leaf_uplink_a_lag_ipv6_local = Column(String(255), nullable=True)
    leaf_uplink_a_lag_ipv6_remote = Column(String(255), nullable=True)
    leaf_uplink_a_lag_ipv6_subnet = Column(String(255), nullable=True)
    leaf_uplink_a_local_ethernet_interfaces = Column(Text(), nullable=True)
    leaf_uplink_a_remote_ethernet_interfaces = Column(Text(), nullable=True)
    leaf_uplink_a_remote_host = Column(String(255), nullable=True)

    leaf_uplink_b_lag_ipv4_local = Column(String(255), nullable=True)
    leaf_uplink_b_lag_ipv4_remote = Column(String(255), nullable=True)
    leaf_uplink_b_lag_ipv4_subnet = Column(String(255), nullable=True)
    leaf_uplink_b_lag_ipv6_local = Column(String(255), nullable=True)
    leaf_uplink_b_lag_ipv6_remote = Column(String(255), nullable=True)
    leaf_uplink_b_lag_ipv6_subnet = Column(String(255), nullable=True)
    leaf_uplink_b_local_ethernet_interfaces = Column(Text(), nullable=True)
    leaf_uplink_b_remote_ethernet_interfaces = Column(Text(), nullable=True)
    leaf_uplink_b_remote_host = Column(String(255), nullable=True)

    dhcp_servers_ipv4 = Column(Text(), nullable=True)
    dhcp_servers_ipv6 = Column(Text(), nullable=True)

    vault_cms_shared_secret_path = Column(String(255), nullable=True)
    vault_cms_shared_secret_last_updated = Column(String(255), nullable=True)
    vault_rip_key_path = Column(String(255), nullable=True)
    vault_rip_key_last_updated = Column(String(255), nullable=True)

    magg_connections_local_ethernet_interfaces = Column(Text(), nullable=True)
    magg_connections_remote_ethernet_interfaces = Column(Text(), nullable=True)
    cust_ip_scope_config_vrf_type = Column(Text(), nullable=True)
    cust_ip_scope_config_vrf_cpe_v4_net = Column(Text(), nullable=True)
    cust_ip_scope_config_vrf_cpe_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_vrf_cm_v4_net = Column(Text(), nullable=True)
    cust_ip_scope_config_vrf_cm_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_cm_scope_v4_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_cm_scope_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_cpe_scope_v4_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_cpe_scope_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_mta_scope_v4_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_mta_scope_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_stb_scope_v6_net = Column(Text(), nullable=True)
    cust_ip_scope_config_an_resi_pd_scope_v6_net = Column(Text(), nullable=True)

    ref_scn_profile_id = Column(UUID, nullable=True)
    ref_scn_profile_name = Column(String(255), nullable=True)

    created_by = Column(String(255), nullable=False)
    updated_by = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utc_timestamp())
    updated_at = Column(DateTime(timezone=True), default=func.utc_timestamp())

    @classmethod
    def from_schema(
        cls,
        schema: schemas.PpodIntentCreate | schemas.PpodIntentUpdate,
        ppod_intent_id: CORE_UUID,
        cpod_intent_id: CORE_UUID = None,
    ) -> "PpodIntent":
        content = {
            "ppod_intent_id": ppod_intent_id,
            "ppod_intent_name": schema.ppod_intent_name,
            "cpod_intent_id": cpod_intent_id,
            "ref_cpod_intent_id": schema.ref_cpod_intent_id,
            "ref_cpod_intent_name": schema.ref_cpod_intent_name,
            "ref_scn_profile_id": schema.ref_scn_profile_id,
            "ref_scn_profile_name": schema.ref_scn_profile_name,
            "updated_by": schema.created_by,
            "created_by": schema.created_by,
        }

        if schema.leaf_uplink:
            content.update(
                {
                    "leaf_uplink_a_lag_ipv4_local": schema.leaf_uplink.leaf_a.lag.ipv4.local,
                    "leaf_uplink_a_lag_ipv4_remote": schema.leaf_uplink.leaf_a.lag.ipv4.remote,
                    "leaf_uplink_a_lag_ipv4_subnet": schema.leaf_uplink.leaf_a.lag.ipv4.subnet,
                    "leaf_uplink_a_lag_ipv6_local": schema.leaf_uplink.leaf_a.lag.ipv6.local,
                    "leaf_uplink_a_lag_ipv6_remote": schema.leaf_uplink.leaf_a.lag.ipv6.remote,
                    "leaf_uplink_a_lag_ipv6_subnet": schema.leaf_uplink.leaf_a.lag.ipv6.subnet,
                    "leaf_uplink_a_local_ethernet_interfaces": ", ".join(
                        [
                            eth.local_interface
                            for eth in schema.leaf_uplink.leaf_a.ethernet_interfaces
                        ]
                    ),
                    "leaf_uplink_a_remote_ethernet_interfaces": ", ".join(
                        [
                            eth.remote_interface
                            for eth in schema.leaf_uplink.leaf_a.ethernet_interfaces
                        ]
                    ),
                    "leaf_uplink_a_remote_host": schema.leaf_uplink.leaf_a.remote_host,
                    "leaf_uplink_b_lag_ipv4_local": schema.leaf_uplink.leaf_b.lag.ipv4.local,
                    "leaf_uplink_b_lag_ipv4_remote": schema.leaf_uplink.leaf_b.lag.ipv4.remote,
                    "leaf_uplink_b_lag_ipv4_subnet": schema.leaf_uplink.leaf_b.lag.ipv4.subnet,
                    "leaf_uplink_b_lag_ipv6_local": schema.leaf_uplink.leaf_b.lag.ipv6.local,
                    "leaf_uplink_b_lag_ipv6_remote": schema.leaf_uplink.leaf_b.lag.ipv6.remote,
                    "leaf_uplink_b_lag_ipv6_subnet": schema.leaf_uplink.leaf_b.lag.ipv6.subnet,
                    "leaf_uplink_b_local_ethernet_interfaces": ", ".join(
                        [
                            eth.local_interface
                            for eth in schema.leaf_uplink.leaf_b.ethernet_interfaces
                        ]
                    ),
                    "leaf_uplink_b_remote_ethernet_interfaces": ", ".join(
                        [
                            eth.remote_interface
                            for eth in schema.leaf_uplink.leaf_b.ethernet_interfaces
                        ]
                    ),
                    "leaf_uplink_b_remote_host": schema.leaf_uplink.leaf_b.remote_host,
                }
            )

        if schema.dhcp_servers:
            content.update(
                {
                    "dhcp_servers_ipv4": ", ".join(schema.dhcp_servers.ipv4),
                    "dhcp_servers_ipv6": ", ".join(schema.dhcp_servers.ipv6),
                }
            )

        if schema.vault:
            content.update(
                {
                    "vault_cms_shared_secret_path": schema.vault.cms_shared_secret.path,
                    "vault_cms_shared_secret_last_updated": schema.vault.cms_shared_secret.last_updated,
                    "vault_rip_key_path": schema.vault.rip_key.path,
                    "vault_rip_key_last_updated": schema.vault.rip_key.last_updated,
                }
            )

        if schema.magg_connections:
            content.update(
                {
                    "magg_connections_local_ethernet_interfaces": ", ".join(
                        [
                            eth.local_interface
                            for eth in schema.magg_connections.ethernet_interfaces
                        ]
                    ),
                    "magg_connections_remote_ethernet_interfaces": ", ".join(
                        [
                            eth.remote_interface
                            for eth in schema.magg_connections.ethernet_interfaces
                        ]
                    ),
                }
            )

        if schema.cust_ip_scope_configuration:
            content.update(
                {
                    "cust_ip_scope_config_vrf_type": ", ".join(
                        [
                            v.vrf_type
                            for v in schema.cust_ip_scope_configuration.vrf_ip_scopes.vrf
                        ]
                    ),
                    "cust_ip_scope_config_vrf_cpe_v4_net": ", ".join(
                        [
                            "|".join(v.cpe_v4_net)
                            for v in schema.cust_ip_scope_configuration.vrf_ip_scopes.vrf
                        ]
                    ),
                    "cust_ip_scope_config_vrf_cpe_v6_net": ", ".join(
                        [
                            "|".join(v.cpe_v6_net)
                            for v in schema.cust_ip_scope_configuration.vrf_ip_scopes.vrf
                        ]
                    ),
                    "cust_ip_scope_config_vrf_cm_v4_net": ", ".join(
                        [
                            "|".join(v.cm_v4_net)
                            for v in schema.cust_ip_scope_configuration.vrf_ip_scopes.vrf
                        ]
                    ),
                    "cust_ip_scope_config_vrf_cm_v6_net": ", ".join(
                        [
                            "|".join(v.cm_v6_net)
                            for v in schema.cust_ip_scope_configuration.vrf_ip_scopes.vrf
                        ]
                    ),
                    "cust_ip_scope_config_an_cm_scope_v4_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.cm_scope_v4_net
                    ),
                    "cust_ip_scope_config_an_cm_scope_v6_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.cm_scope_v6_net
                    ),
                    "cust_ip_scope_config_an_cpe_scope_v4_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.cpe_scope_v4_net
                    ),
                    "cust_ip_scope_config_an_cpe_scope_v6_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.cpe_scope_v6_net
                    ),
                    "cust_ip_scope_config_an_mta_scope_v4_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.mta_scope_v4_net
                    ),
                    "cust_ip_scope_config_an_mta_scope_v6_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.mta_scope_v6_net
                    ),
                    "cust_ip_scope_config_an_stb_scope_v6_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.stb_scope_v6_net
                    ),
                    "cust_ip_scope_config_an_resi_pd_scope_v6_net": ", ".join(
                        schema.cust_ip_scope_configuration.vrf_ip_scopes.an_ipscopes.resi_pd_scope_v6_net
                    ),
                }
            )

        return cls(**content)

    def to_schema(self) -> schemas.SiteIntentReturn:
        content = {
            "ppod_intent_id": self.ppod_intent_id,
            "cpod_intent_id": self.cpod_intent_id,
            "ppod_intent_name": self.ppod_intent_name,
            "ref_cpod_intent_name": self.ref_cpod_intent_name,
            "leaf_uplink": None,
            "dhcp_servers": None,
            "vault": None,
            "magg_connections": None,
            "cust_ip_scope_configuration": None,
            "ref_scn_profile_id": self.ref_scn_profile_id,
            "ref_scn_profile_name": self.ref_scn_profile_name,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        return schemas.PpodIntentReturn.model_validate(
            content, by_name=True
        ).model_dump(by_alias=True)
