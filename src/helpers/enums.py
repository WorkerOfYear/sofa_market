from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class PurchaseStatusEnum(BaseEnum):
    CREATED = "CREATED"
    PROCESSED = "PROCESSED"


class ImageStorageTypeEnum(BaseEnum):
    LOCAL = "LOCAL"
    S3 = "S3"
    YANDEX = "YANDEX"
