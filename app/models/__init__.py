# from pydantic import BaseModel, Field, field_validator
# from fastapi.encoders import jsonable_encoder
#
#
# class EthernetInterfaces(BaseModel):
#     local_interface: str = Field(alias="localInterface")
#     remote_interface: str = Field(alias="remoteInterface")
#
#
# class Leaf(BaseModel):
#     ethernet_interfaces: list[EthernetInterfaces] | list[dict] = Field(
#         alias="ethernetInterfaces"
#     )
#     remote_host: str = Field(alias="remoteHost")
#
#     # @field_validator("ethernet_interfaces")
#     # def manage_ethernet_interfaces(cls, value: list[EthernetInterfaces] | list[dict]):
#     #     if isinstance(value[0], EthernetInterfaces):
#     #         print(1)
#     #         value = [v.model_dump() for v in value]
#     #     elif isinstance(value[0], dict):
#     #         print(2)
#     #         for v in value:
#     #             EthernetInterfaces.model_validate(v, by_name=True)
#     #
#     #     return value
#
#
# content = {
#     "ethernet_interfaces": [
#         {
#             "local_interface": "first-local",
#             "remote_interface": "first-remote",
#         },
#         {
#             "local_interface": "second-local",
#             "remote_interface": "second-remote",
#         },
#     ],
#     "remote_host": "remote_host",
# }
#
# out = Leaf.model_validate(content, by_name=True)
# print(out.model_dump(by_alias=True))
