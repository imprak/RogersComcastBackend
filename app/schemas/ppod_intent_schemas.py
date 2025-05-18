from datetime import datetime
from typing import List, Optional

from pydantic import Field, UUID4, BaseModel


class Ip(BaseModel):
    local: str
    remote: str
    subnet: str


class Lag(BaseModel):
    ipv4: Ip
    ipv6: Ip


class EthernetInterfaces(BaseModel):
    local_interface: str = Field(alias="localInterface")
    remote_interface: str = Field(alias="remoteInterface")


class Leaf(BaseModel):
    lag: Lag
    ethernet_interfaces: List[EthernetInterfaces] = Field(alias="ethernetInterfaces")
    remote_host: str = Field(alias="remoteHost")


class LeafUplink(BaseModel):
    leaf_a: Leaf = Field(alias="leafA")
    leaf_b: Leaf = Field(alias="leafB")


class DhcpServers(BaseModel):
    ipv4: List[str]
    ipv6: List[str]


class CredInfo(BaseModel):
    path: str
    last_updated: str = Field(alias="lastUpdated")


class Vault(BaseModel):
    cms_shared_secret: CredInfo = Field(alias="cmSharedSecret")
    rip_key: CredInfo = Field(alias="ripKey")


class MaggConnections(BaseModel):
    ethernet_interfaces: List[EthernetInterfaces] = Field(alias="ethernetInterfaces")


class AnIpscopes(BaseModel):
    cm_scope_v4_net: List[str]
    cm_scope_v6_net: List[str]
    cpe_scope_v4_net: List[str]
    cpe_scope_v6_net: List[str]
    mta_scope_v4_net: List[str]
    mta_scope_v6_net: List[str]
    stb_scope_v6_net: List[str]
    resi_pd_scope_v6_net: List[str]


class Vrf(BaseModel):
    vrf_type: str = Field(None, alias="vrfType")
    cpe_v4_net: List[str] = Field(None)
    cpe_v6_net: List[str] = Field(None)
    cm_v4_net: List[str] = Field(None)
    cm_v6_net: List[str] = Field(None)


class VrfIPScopes(BaseModel):
    vrf: List[Vrf]
    an_ipscopes: AnIpscopes = Field(alias="anIpscopes")


class CustIpScopeConfiguration(BaseModel):
    vrf_ip_scopes: VrfIPScopes = Field(alias="vrfIPScopes")


class PpodIntentBase(BaseModel):
    ppod_intent_name: str = Field(alias="ppodIntentName")
    ref_cpod_intent_name: str = Field(alias="refCpodIntentName")
    leaf_uplink: Optional[LeafUplink] = Field(None, alias="leafUplink")
    dhcp_servers: Optional[DhcpServers] = Field(None, alias="dhcpServers")
    vault: Optional[Vault] = Field(None)
    magg_connections: Optional[MaggConnections] = Field(None, alias="maggConnections")
    cust_ip_scope_configuration: Optional[CustIpScopeConfiguration] = Field(
        None, alias="custIpScopeConfiguration"
    )
    ref_scn_profile_id: Optional[UUID4] = Field(
        None, examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refScnProfileId"
    )
    ref_scn_profile_name: Optional[str] = Field(None, alias="refScnProfileName")

    created_by: str = Field(None, alias="createdBy", exclude=True)
    updated_by: str = Field(None, alias="updatedBy", exclude=True)


class PpodIntentCreate(PpodIntentBase):
    ref_cpod_intent_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refCpodIntentId"
    )


class PpodIntentUpdate(PpodIntentBase):
    ref_cpod_intent_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="refCpodIntentId"
    )


class PpodIntentReturn(PpodIntentBase):
    ppod_intent_id: UUID4 = Field(
        examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="ppodIntentId"
    )
    cpod_intent_id: Optional[UUID4] = Field(
        None, examples=["554aab05-dd7f-44ec-be0c-749eb083505c"], alias="cpodIntentId"
    )

    created_by: str = Field(alias="createdBy")
    updated_by: str = Field(alias="updatedBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
