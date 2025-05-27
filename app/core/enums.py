from enum import Enum


class TransactionStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(str, Enum):
    SINGLE = "single"
    BULK = "bulk"


class OrderStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ApiNameEnums(str, Enum):
    HUB = "hub"
    SITE_INTENT = "site_intent"
    PPOD_INTENT = "ppod_intent"
    CPOD_INTENT = "cpod_intent"
    BUHM = "buhm"
    HAGG_INTENT = "hagg_intent"
    DAAS_INTENT = "daas_intent"
    REMOTE_PHY_INTENT = "remote_phy_intent"
    SPECTRUM_RECOMMENDATION = "spectrum_recommendation"
    VIDEO_CONFIGURATION = "video_configuration"
    ACTIVATE_FIELD_RDP = "activate_field_rdp"
    ACTIVATE_SHELF_RDP = "activate_shelf_rdp"
    SCN_PROFILE = "scn_profile"
    SERVICE_CLASS = "service_class"
    SERVICE_CLASS_QOS = "service_class_qos"
    SERVICE_CLASS_VALUE = "service_class_value"


