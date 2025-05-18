from enum import Enum


class TransactionStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(str, Enum):
    SINGLE = "single"
    BULK = "bulk"