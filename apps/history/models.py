from django.db import models
from django.conf import settings


class History(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='유저'
    )
    

    class Meta:
        db_table = 'history'
        verbose_name = '이력'
        verbose_name_plural = '이력들'

