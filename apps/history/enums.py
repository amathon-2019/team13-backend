from enum import IntEnum


class DeviceType(IntEnum):
    DESKTOP = 0
    MOBILE = 1

    @classmethod
    def choices(cls):
        return (
            (cls.DESKTOP.value, '데스크탑'),
            (cls.MOBILE.value, '모바일'),
        )
