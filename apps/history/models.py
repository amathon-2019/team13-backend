from django.db import models
from .enums import DeviceType


class History(models.Model):
    token = models.OneToOneField(
        'user.Token',
        on_delete=models.CASCADE,
        verbose_name='토큰'
    )
    device = models.SmallIntegerField(
        '디바이스',
        choices=DeviceType.choices(),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        '활성화 여부',
        default=True
    )
    created = models.DateTimeField(
        '생성일',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        '수정일',
        auto_now=True
    )

    class Meta:
        db_table = 'history'
        verbose_name = '이력'
        verbose_name_plural = '이력들'

